from flask import Blueprint, render_template, request, redirect, url_for
from app.models.tables import Oficina, Aluno, Usuario
from app.models.forms import CadastroOficinaForm
from app.ext.db import db
from flask_login import login_required, current_user

bp_app = Blueprint("oficina", __name__)
route_prefix = "/oficina"

@bp_app.route(route_prefix+"/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroOficinaForm()
    form.responsavel.choices = [(usuario.id, usuario.nome) for usuario in Usuario.query.all()]
    if form.validate_on_submit():
        oficina = Oficina()
        oficina = form.populate_obj(oficina)
        db.session.add(oficina)
        db.session.commit()
        return redirect(url_for("oficina.lista"))

    return render_template("oficina/cadastro.html", form=form, action=url_for('oficina.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@login_required
def lista():
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    if current_user.role == "responsavel":
        oficinas = Oficina.query.filter_by(responsavel_id=current_user.id).all()
    else:
        oficinas = Oficina.query.all()

    return render_template("oficina/lista.html", oficinas=oficinas)


@bp_app.route(route_prefix+"/calendario")
@login_required
def calendario():
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    oficinas = Oficina.query.all()
    return render_template("oficina/calendario.html", oficinas=oficinas)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroOficinaForm()
    oficina = Oficina.query.filter_by(id=id).first()
    form.responsavel.choices = [(usuario.id, usuario.nome) for usuario in Usuario.query.all()]

    if form.validate_on_submit():
        oficina = form.populate_obj(oficina)
        db.session.commit()
        return redirect(url_for("oficina.lista"))

    form.insert_data(oficina)

    return render_template("oficina/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=id).first()

    db.session.delete(oficina)
    db.session.commit()

    return redirect(url_for("oficina.lista"))


@bp_app.route(route_prefix+"/matricula/<int:oficinaid>")
@login_required
def matricula(oficinaid):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    alunos = Aluno.query.all()
    return render_template("oficina/matricula.html", oficina=oficina, alunos=alunos)


@bp_app.route(route_prefix+"/matricular/<int:oficinaid>/<int:alunoid>")
@login_required
def matricular(oficinaid, alunoid):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    aluno = Aluno.query.filter_by(id=alunoid).first()
    
    oficina.alunos.append(aluno)
    db.session.commit()

    return redirect(url_for("oficina.matricula", oficinaid=oficinaid))


@bp_app.route(route_prefix+"/desmatricular/<int:oficinaid>/<int:alunoid>")
@login_required
def desmatricular(oficinaid, alunoid):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    aluno = Aluno.query.filter_by(id=alunoid).first()
    
    oficina.alunos.remove(aluno)
    db.session.commit()

    return redirect(url_for("oficina.matricula", oficinaid=oficinaid))

@bp_app.route(route_prefix+"/boletim/<int:id>")
@login_required
def boletim(id):
    if not current_user.permissao("responsavel"):
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=id).first()

    return render_template("oficina/boletim.html", oficina=oficina)

def configure(app):
    app.register_blueprint(bp_app)