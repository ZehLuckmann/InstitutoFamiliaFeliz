from flask import Blueprint, render_template, request, redirect, url_for
from app.models.tables import Aluno
from app.models.forms import CadastroAlunoForm
from app.ext.db import db
from flask_login import login_required, current_user
from config import UPLOAD_FOLDER, BASE_DIR
import os

bp_app = Blueprint("aluno", __name__)
route_prefix="/aluno"

@bp_app.route(route_prefix+"/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroAlunoForm()
    if form.validate_on_submit():
        aluno = Aluno()
        form.populate_obj(aluno)
        db.session.add(aluno)
        db.session.commit()
        db.session.refresh(aluno)
        if form.foto.data:
            form.foto.data.save(f"{UPLOAD_FOLDER}/alunos/fotos/{str(aluno.id)}.png")
        return redirect(url_for("aluno.lista")) 

    return render_template("aluno/cadastro.html", form=form, action=url_for('aluno.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@login_required
def lista():
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    alunos = Aluno.query.all()

    return render_template("aluno/lista.html", alunos=alunos)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroAlunoForm()
    aluno = Aluno.query.filter_by(id=id).first()

    if form.validate_on_submit():
        form.populate_obj(aluno)
        if form.foto.data:
            form.foto.data.save(f"{UPLOAD_FOLDER}/alunos/fotos/{str(aluno.id)}.png")
        db.session.commit()
        return redirect(url_for("aluno.lista"))
        
    form.insert_data(aluno)

    return render_template("aluno/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))
        
    aluno = Aluno.query.filter_by(id=id).first()

    db.session.delete(aluno)
    db.session.commit()

    return redirect(url_for("aluno.lista"))

@bp_app.route(route_prefix+"/boletim/<int:id>")
@login_required
def boletim(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    aluno = Aluno.query.filter_by(id=id).first()
    oficinas = aluno.oficinas
    return render_template("aluno/boletim.html", aluno=aluno)

def configure(app):
    app.register_blueprint(bp_app)