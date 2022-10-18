from xmlrpc.client import Boolean
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.tables import Aula, Oficina, Frequencia
from app.models.forms import CadastroAulaForm
from app.ext.db import db
from flask_login import login_required, current_user

bp_app = Blueprint("aula", __name__)
route_prefix = "/aula"

@bp_app.route(route_prefix+"/cadastrar/", methods=["GET", "POST"])
@login_required
def cadastrar():
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroAulaForm()
    form.oficina.choices = [(oficina.id, oficina.nome) for oficina in Oficina.query.all()]
    
    if form.validate_on_submit():
        aula = Aula()
        aula = form.populate_obj(aula)
        db.session.add(aula)
        db.session.commit()
        db.session.refresh(aula)


        frequencia = []
        oficina = Oficina.query.filter_by(id=aula.oficina_id).first()
        for aluno in oficina.alunos:
            frequencia.append(Frequencia(aula_id=aula.id, aluno_id=aluno.id))

        db.session.bulk_save_objects(frequencia)
        db.session.commit()


        return redirect(url_for("aula.lista"))

    return render_template("aula/cadastro.html", form=form, action=url_for('aula.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@bp_app.route(route_prefix+"/lista/<int:oficinaid>")
@login_required
def lista(oficinaid=-1):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    aulas = Aula.query
    if oficinaid != -1:
        aulas = aulas.filter_by(oficina_id=oficinaid)
    if current_user.role=="responsavel":
        oficinas = [r.id for r in Oficina.query.filter_by(responsavel_id=current_user.id).all()]
        print(oficinas)
        aulas = aulas.filter(Aula.oficina_id.in_(oficinas))
    aulas = aulas.order_by(Aula.data.desc()).all()

    return render_template("aula/lista.html", aulas=aulas)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroAulaForm()
    form.oficina.choices = [(oficina.id, oficina.nome) for oficina in Oficina.query.all()]
    
    aula = Aula.query.filter_by(id=id).first()

    if form.validate_on_submit():
        aula = form.populate_obj(aula)
        db.session.commit()
        return redirect(url_for("aula.lista"))

    form.insert_data(aula)
    return render_template("aula/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    aula = Aula.query.filter_by(id=id).first()

    db.session.delete(aula)
    db.session.commit()
    return redirect(url_for("aula.lista"))

@bp_app.route(route_prefix+"/frequencia/<int:aulaid>")
@login_required
def frequencia(aulaid):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    frequencias = Frequencia.query.filter_by(aula_id=aulaid).all()
    return render_template("aula/frequencia.html", frequencias=frequencias)

@bp_app.route(route_prefix+"/frequencia")
#@login_required
def presenca():
    #if not current_user.permissao("coordenador"):
    #    return redirect(url_for("usuario.acesso_negado"))
    freq_id = request.args.get('freq_id', -1, type=int)
    presenca = request.args.get('presenca', "true")=="true"
    frequencia = Frequencia.query.filter_by(id=freq_id).first()
    if frequencia:
        frequencia.presenca = presenca
        db.session.commit()

    return jsonify(result=[freq_id, presenca] )

def configure(app):
    app.register_blueprint(bp_app)