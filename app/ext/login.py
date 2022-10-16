from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from app.models.tables import Usuario
from app.ext.db import db

def create_user(nome, login, role):
    user = Usuario.query.filter_by(login=login).first()
    if not user:
        user = Usuario(nome=nome, login=login, senha=generate_password_hash(login), role=role)
        db.session.add(user)
        db.session.commit()


def configure(app):
    login_manager = LoginManager()
    login_manager.login_view = 'usuario.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return Usuario.query.get(int(userid))

    #Role and Users
    try:
        with app.app_context():
            create_user("Administrador", "admin", "admin")
    except:
        print("Erro ao criar usuario adm")