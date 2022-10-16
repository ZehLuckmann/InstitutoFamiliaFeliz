from flask import Blueprint, render_template, request, redirect, url_for
from app.models.tables import Oficina, Aluno
from app.models.forms import CadastroOficinaForm
from app.ext.db import db
from flask_login import login_required, current_user

bp_app = Blueprint("oficina", __name__)
route_prefix = "/oficina"

@bp_app.route(route_prefix+"/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroOficinaForm()
    if form.validate_on_submit():
        p = Oficina()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("oficina.lista"))

    return render_template("oficina/cadastro.html", form=form, action=url_for('oficina.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@login_required
def lista():
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficinas = Oficina.query.all()
    return render_template("oficina/lista.html", oficinas=oficinas)


@bp_app.route(route_prefix+"/calendario")
@login_required
def calendario():
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficinas = Oficina.query.all()
    return render_template("oficina/calendario.html", oficinas=oficinas)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroOficinaForm()
    oficina = Oficina.query.filter_by(id=id).first()

    if form.validate_on_submit():
        form.populate_obj(oficina)
        db.session.commit()
        return redirect(url_for("oficina.lista"))


    form = CadastroOficinaForm()
    form.insert_data(oficina)

    return render_template("oficina/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=id).first()

    db.session.delete(oficina)
    db.session.commit()

    return redirect(url_for("oficina.lista"))


@bp_app.route(route_prefix+"/matricula/<int:oficinaid>")
@login_required
def matricula(oficinaid):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    alunos = Aluno.query.all()
    return render_template("oficina/matricula.html", oficina=oficina, alunos=alunos)


@bp_app.route(route_prefix+"/matricular/<int:oficinaid>/<int:alunoid>")
@login_required
def matricular(oficinaid, alunoid):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    aluno = Aluno.query.filter_by(id=alunoid).first()
    
    oficina.alunos.append(aluno)
    db.session.commit()

    return redirect(url_for("oficina.matricula", oficinaid=oficinaid))


@bp_app.route(route_prefix+"/desmatricular/<int:oficinaid>/<int:alunoid>")
@login_required
def desmatricular(oficinaid, alunoid):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    oficina = Oficina.query.filter_by(id=oficinaid).first()
    aluno = Aluno.query.filter_by(id=alunoid).first()
    
    oficina.alunos.remove(aluno)
    db.session.commit()

    return redirect(url_for("oficina.matricula", oficinaid=oficinaid))

def configure(app):
    app.register_blueprint(bp_app)