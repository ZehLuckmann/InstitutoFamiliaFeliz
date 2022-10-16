from flask import Blueprint, render_template, request, redirect, url_for
from app.models.tables import Aluno
from app.models.forms import DashboardGeralForm
from app.ext.db import db
from flask_login import login_required

bp_app = Blueprint("home", __name__)


@bp_app.route("/")
@bp_app.route("/home")
@login_required
def home():
    form = DashboardGeralForm()
    form.calcular()
    return render_template("index.html", form=form)

def configure(app):
    app.register_blueprint(bp_app)
