from email.policy import default
from app.ext.db import db
from datetime import datetime
from datetime import date
from app.models.utils import daterange, DIAS_SEMANA, GENERO
from flask_login import UserMixin
from flask import url_for
from os.path import exists
from config import UPLOAD_FOLDER
from sqlalchemy.orm.session import object_session 

class Aluno(db.Model):
    __tablename__ = "aluno"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    sobrenome = db.Column(db.String)
    genero = db.Column(db.String)
    escola = db.Column(db.String)
    ano = db.Column(db.String)
    rua = db.Column(db.String)
    numero = db.Column(db.String)
    bairro = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    fone = db.Column(db.String)
    cpf = db.Column(db.String)
    genero = db.Column(db.String)
    pai = db.Column(db.String)
    mae = db.Column(db.String)
    fone_pai = db.Column(db.String)
    fone_mae = db.Column(db.String)

     
    def calcula_presenca(self, oficina_id):
        presenca = len([freq for freq in self.frequencia if (freq.aula.oficina.id == oficina_id) & (freq.presenca == True)])
        return presenca

    def calcula_ausencia(self, oficina_id):
        ausencia = len([freq for freq in self.frequencia if (freq.aula.oficina.id == oficina_id) & (freq.presenca == False)])
        return ausencia

    def calcula_percentual_presenca(self, oficina_id):
        presenca = len([freq for freq in self.frequencia if (freq.aula.oficina.id == oficina_id) & (freq.presenca == True)])
        total = len([freq for freq in self.frequencia if (freq.aula.oficina.id == oficina_id)])

        return (presenca*100)/total if total > 0 else 0.0

    @property
    def foto_url(self):
        url = url_for('static', filename=f'uploads/alunos/fotos/{self.id}.png')
        if not exists(f"{UPLOAD_FOLDER}/alunos/fotos/{str(self.id)}.png"):
            url = url_for('static', filename=f'images/icon/default-avatar.png')
        return url

    @property
    def genero_str(self):
        r = [item for item in GENERO if self.genero in item]
        return r[0][1]

#Biblioteca
class Livro(db.Model):
    __tablename__ = "livro"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    codigo = db.Column(db.String)
    sub_codigo = db.Column(db.String)

    @property
    def status(self):
        emprestimos = EmprestimoLivro.query.filter_by(livro_id=self.id).filter(EmprestimoLivro.data_devolucao == None).all()
        return len(emprestimos)<1 

    @property
    def emprestimos_abertos(self):
        return EmprestimoLivro.query.filter_by(livro_id=self.id).filter(EmprestimoLivro.data_devolucao == None).all()

class EmprestimoLivro(db.Model):
    __tablename__ = "emprestimo_livro"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'))
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))

    livro = db.relationship('Livro', lazy='subquery', backref=db.backref('emprestimo_livro', lazy=True))
    aluno = db.relationship('Aluno', lazy='subquery', backref=db.backref('emprestimo_livro', lazy=True))
    data_emprestimo = db.Column(db.Date)
    data_devolucao = db.Column(db.Date)


#Oficina
matricula = db.Table('matricula',
    db.Column('aluno', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
    db.Column('oficina', db.Integer, db.ForeignKey('oficina.id'), primary_key=True)
)


class Oficina(db.Model):
    __tablename__ = "oficina"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    inicio = db.Column(db.Date)
    fim = db.Column(db.Date)
    dia_semana = db.Column(db.String)
    horario = db.Column(db.Time)
    
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    aula = db.relationship('Aula', backref='oficina')
    alunos = db.relationship('Aluno', secondary=matricula, lazy='subquery', backref=db.backref('oficinas', lazy=True))

    @property
    def dia_semana_str(self):
        r = [item for item in DIAS_SEMANA if self.dia_semana in item]
        return r[0][1]

    @property
    def total_alunos(self):
        return len(self.alunos)

    @property
    def total_aulas(self):
        return len(self.aula)

    @property
    def datas_futuras(self):
        datas = []
        for single_date in daterange(date.today(), self.fim):
           if str(single_date.weekday()) == self.dia_semana:
                single_date = datetime.combine(single_date, self.horario)
                datas.append([self.nome, single_date.isoformat()])

        return datas

class Aula(db.Model):
    __tablename__ = "aula"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    oficina_id = db.Column(db.Integer, db.ForeignKey('oficina.id'))
    data = db.Column(db.Date)
    horario = db.Column(db.Time)

    @property
    def data_iso(self):
        return datetime.combine(self.data, self.horario).isoformat()

class Frequencia(db.Model):
    __tablename__ = "frequencia"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aula_id = db.Column(db.Integer, db.ForeignKey('aula.id'))
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'))

    aula = db.relationship('Aula', lazy='subquery', backref=db.backref('frequencia', lazy=True))
    aluno = db.relationship('Aluno', lazy='subquery', backref=db.backref('frequencia', lazy=True))
    presenca = db.Column('presenca', db.Boolean, default=False)

    @property
    def total_alunos(self):
        return len(self.alunos)

#usuarios
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    nome = db.Column(db.String(1000))
    role = db.Column(db.String)
    oficinas = db.relationship('Oficina', backref='responsavel')

    @property
    def foto_url(self):
        url = url_for('static', filename=f'uploads/usuarios/fotos/{self.id}.png')
        if not exists(f"{UPLOAD_FOLDER}/usuarios/fotos/{str(self.id)}.png"):
            url = url_for('static', filename=f'images/icon/default-avatar.png')
        return url
    
    def permissao(self, role):
        if role == "admin": 
            return self.role in ["admin"]
        elif role == "coordenador":
            return self.role in ["admin", "coordenador"]
        elif role == "responsavel":
            return self.role in ["admin", "coordenador", "responsavel"]
        return False
