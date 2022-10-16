from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.tables import Usuario
from app.models.forms import LoginForm, CadastroUsuarioForm
from app.ext.db import db
from flask_login import login_user, logout_user, login_required, current_user
from config import UPLOAD_FOLDER

bp_app = Blueprint("usuario", __name__)
route_prefix = "/usuario"

@bp_app.route(route_prefix+"/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroUsuarioForm()
    if form.validate_on_submit():
        p = Usuario()
        form.populate_obj(p)
        p.senha = generate_password_hash(p.senha)
        db.session.add(p)
        db.session.commit()
        db.session.refresh(p)
        if form.foto.data:
            form.foto.data.save(f"{UPLOAD_FOLDER}/usuarios/fotos/{str(p.id)}.png")
        return redirect(url_for("usuario.lista"))
    return render_template("usuario/cadastro.html", form=form, action=url_for('usuario.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@login_required
def lista():
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    usuarios = Usuario.query.all()
    return render_template("usuario/lista.html", usuarios=usuarios)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    print(current_user.id, id)
    if (current_user.role not in ["admin"]) & (current_user.id != id):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroUsuarioForm()
    usuario = Usuario.query.filter_by(id=id).first()

    if form.validate_on_submit():
        form.populate_obj(usuario)
        db.session.commit()
        if form.foto.data:
            form.foto.data.save(f"{UPLOAD_FOLDER}/usuarios/fotos/{str(usuario.id)}.png")
        return redirect(url_for("usuario.lista"))

    form = CadastroUsuarioForm()
    form.insert_data(usuario)
    return render_template("usuario/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if current_user.role not in ["admin"]:
        return redirect(url_for("usuario.acesso_negado"))

    usuario = Usuario.query.filter_by(id=id).first()

    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for("usuario.lista"))

@bp_app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(login=form.login.data).first()
        print(usuario)
        if not usuario or not check_password_hash(usuario.senha, form.senha.data):
            return redirect(url_for('usuario.login'))

        login_user(usuario, remember=True)
        return redirect(url_for('home.home'))

    return render_template("usuario/login.html", form=form)

@bp_app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('usuario.login'))

@bp_app.route("/403")
@login_required
def acesso_negado():
    return render_template("usuario/403.html")

def configure(app):
    app.register_blueprint(bp_app)
