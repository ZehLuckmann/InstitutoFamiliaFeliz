from distutils.command.upload import upload
from flask import Flask
from app.ext import db, migrate, login, uploads
from app.blueprints import home, aluno, livro, oficina, usuario, aula


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    
    # Extensions
    db.configure(app)
    migrate.configure(app)
    login.configure(app)
    uploads.configure(app)

    # Blueprints
    home.configure(app)
    aluno.configure(app)
    livro.configure(app)
    oficina.configure(app)
    usuario.configure(app)
    aula.configure(app)

    return app
