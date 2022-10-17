from flask import Blueprint, render_template, request, redirect, url_for
from app.models.tables import EmprestimoLivro, Livro, Aluno
from app.models.forms import CadastroLivroForm, CadastroEmprestimoLivroForm
from app.ext.db import db
from flask_login import login_required, current_user

bp_app = Blueprint("livro", __name__)
route_prefix = "/livro"

@bp_app.route(route_prefix+"/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroLivroForm()
    if form.validate_on_submit():
        p = Livro()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("livro.lista"))

    return render_template("livro/cadastro.html", form=form, action=url_for('livro.cadastrar'))


@bp_app.route(route_prefix+"/lista")
@login_required
def lista():
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    livros = Livro.query.all()
    return render_template("livro/lista.html", livros=livros)


@bp_app.route(route_prefix+"/atualizar/<int:id>", methods=["GET", "POST"])
@login_required
def atualizar(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroLivroForm()
    livro = Livro.query.filter_by(id=id).first()

    if form.validate_on_submit():
        form.populate_obj(livro)
        db.session.commit()
        return redirect(url_for("livro.lista"))

    form.insert_data(livro)
    return render_template("livro/cadastro.html", form=form)


@bp_app.route(route_prefix+"/excluir/<int:id>")
@login_required
def excluir(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    livro = Livro.query.filter_by(id=id).first()

    db.session.delete(livro)
    db.session.commit()
    return redirect(url_for("livro.lista"))

@bp_app.route(route_prefix+"/emprestimo", methods=["GET", "POST"])
@bp_app.route(route_prefix+"/emprestimo/<int:livroid>", methods=["GET", "POST"])
@login_required
def emprestimo(livroid=-1):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroEmprestimoLivroForm()
    
    form.aluno.choices = [(aluno.id, aluno.nome) for aluno in Aluno.query.all()]
    form.livro.choices = [(livro.id, livro.nome) for livro in Livro.query.all()]

    if form.validate_on_submit():
        p = EmprestimoLivro()
        p.data_emprestimo = form.data_emprestimo.data
        p.data_devolucao = form.data_devolucao.data
        p.aluno_id = form.aluno.data
        p.livro_id = form.livro.data
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("livro.lista"))
    
    
    form.livro.data = livroid
    return render_template("livro/emprestimo.html", form=form, action=url_for('livro.emprestimo'))

@bp_app.route(route_prefix+"/devolucao/<int:id>", methods=["GET", "POST"])
@login_required
def devolucao(id):
    if not current_user.permissao("coordenador"):
        return redirect(url_for("usuario.acesso_negado"))

    form = CadastroEmprestimoLivroForm()
    form.aluno.choices = [(aluno.id, aluno.nome) for aluno in Aluno.query.all()]
    form.livro.choices = [(livro.id, livro.nome) for livro in Livro.query.all()]
    
    emprestimo_livro = EmprestimoLivro.query.filter_by(id=id).first()

    if form.validate_on_submit():
        emprestimo_livro.data_emprestimo = form.data_emprestimo.data
        emprestimo_livro.data_devolucao = form.data_devolucao.data
        emprestimo_livro.aluno_id = form.aluno.data
        emprestimo_livro.livro_id = form.livro.data
        db.session.commit()
        return redirect(url_for("livro.lista"))

    form.insert_data(emprestimo_livro)
    return render_template("livro/emprestimo.html", form=form)

def configure(app):
    app.register_blueprint(bp_app)