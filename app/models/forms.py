from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Optional

from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import datetime
from app.models.utils import DIAS_SEMANA, CSS_CLASS_FIELD, GENERO, ROLES, inicio_semestre_atual, fim_semestre_atual
from app.models.tables import Aluno, Aula, Oficina, Livro

 

class CadastroAlunoForm(FlaskForm):
    csnpo = StringField("CSNPO:", validators=[])
    nome = StringField("Nome:", validators=[DataRequired()])
    sobrenome = StringField("Sobrenome:", validators=[DataRequired()])
    escola = StringField("Escola:", validators=[])
    ano = StringField("Ano:", validators=[])
    rua = StringField("Rua:", validators=[])
    numero = StringField("Número:", validators=[])
    bairro = StringField("Bairro:", validators=[])
    cidade = StringField("Cidade:", validators=[])
    estado = StringField("Estado:", validators=[])
    fone = StringField("Telefone:", validators=[])
    cpf = StringField("Cpf:", validators=[])
    foto = FileField(validators=[])
    genero = SelectField("Gênero:", choices=GENERO, validators=[DataRequired()])  
    fone_pai = StringField("Telefone:", validators=[])
    fone_mae = StringField("Telefone:", validators=[])
    pai = StringField("Pai:", validators=[])
    mae = StringField("Mãe:", validators=[])
    observacoes = TextAreaField("Observações:", validators=[])

    def insert_data(self, aluno):
        self.nome.data = aluno.nome
        self.csnpo.data = aluno.csnpo
        self.sobrenome.data = aluno.sobrenome
        self.escola.data = aluno.escola
        self.ano.data = aluno.ano
        self.rua.data = aluno.rua
        self.numero.data = aluno.numero
        self.bairro.data = aluno.bairro
        self.cidade.data = aluno.cidade
        self.estado.data = aluno.estado
        self.fone.data = aluno.fone
        self.cpf.data = aluno.cpf
        self.fone_pai.data = aluno.fone_pai
        self.fone_mae.data = aluno.fone_mae
        self.pai.data = aluno.pai
        self.mae.data = aluno.mae
        self.genero.data = aluno.genero
        self.observacoes.data = aluno.observacoes


class CadastroLivroForm(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    codigo = StringField("Código:", validators=[DataRequired()])
    sub_codigo = StringField("Sub Código:", validators=[DataRequired()])
    
    def insert_data(self, livro):
        self.nome.data = livro.nome
        self.codigo.data = livro.codigo
        self.sub_codigo.data = livro.sub_codigo

class CadastroEmprestimoLivroForm(FlaskForm):
    data_emprestimo = DateField("Data Emprestimo:", validators=[DataRequired()], format='%d/%m/%Y', default=datetime.now())
    data_devolucao = DateField("Data Devoluçãos:", validators=[Optional(strip_whitespace=True)], format='%d/%m/%Y')
    aluno = SelectField('Aluno:',choices=[], coerce=int, validators=[], render_kw={'class': CSS_CLASS_FIELD + " select2"})
    livro = SelectField('Livro:',choices=[], coerce=int, validators=[], render_kw={'class': CSS_CLASS_FIELD + " select2"})
    
    def insert_data(self, emprestimo_livro):
        self.data_emprestimo.data = emprestimo_livro.data_emprestimo
        self.data_devolucao.data = emprestimo_livro.data_devolucao
        self.aluno.data = emprestimo_livro.aluno_id
        self.livro.data = emprestimo_livro.livro_id

class CadastroOficinaForm(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    inicio = DateField("Data Inicio:", validators=[DataRequired()], format='%d/%m/%Y', default=inicio_semestre_atual())
    fim = DateField("Data Fim:", validators=[DataRequired()], format='%d/%m/%Y', default=fim_semestre_atual())
    dia_semana = SelectField("Dia da Semana:", choices=DIAS_SEMANA, validators=[DataRequired()])
    horario = TimeField("Horario:", format='%H:%M', validators=[DataRequired()])
    responsavel = SelectField('Responsavel:',choices=[], coerce=int)

    def insert_data(self, oficina):
        self.nome.data = oficina.nome
        self.inicio.data = oficina.inicio
        self.fim.data = oficina.fim
        self.dia_semana.data = oficina.dia_semana
        self.horario.data = oficina.horario
        self.responsavel.data = oficina.responsavel_id
    
    def populate_obj(self, oficina):
        oficina.nome = self.nome.data 
        oficina.inicio = self.inicio.data 
        oficina.fim = self.fim.data 
        oficina.dia_semana = self.dia_semana.data 
        oficina.horario = self.horario.data
        oficina.responsavel_id = self.responsavel.data
        return oficina

class CadastroAulaForm(FlaskForm):
    data = DateField("Data Inicio:", validators=[DataRequired()], format='%d/%m/%Y', default=datetime.now())
    oficina = SelectField('Oficina:',choices=[], coerce=int)
    horario = TimeField("Horario:", format='%H:%M', validators=[DataRequired()])
    plano_aula = TextAreaField("Plano de aula:", validators=[])
    
    def insert_data(self, aula):
        self.data.data = aula.data
        self.oficina.data = aula.oficina
        self.horario.data = aula.horario

    def populate_obj(self, aula):
        aula.data = self.data.data
        aula.oficina_id = self.oficina.data
        aula.horario = self.horario.data
        aula.plano_aula = self.plano_aula.data
        return aula

class CadastroUsuarioForm(FlaskForm):
    nome = StringField("Nome:", validators=[DataRequired()])
    login = StringField("Login:", validators=[DataRequired()])
    senha = PasswordField("Senha:", validators=[DataRequired()])
    role = SelectField("Cargo:", choices=ROLES, validators=[DataRequired()])
    foto = FileField(validators=[])
    
    def insert_data(self, usuario):
        self.nome.data = usuario.nome
        self.login.data = usuario.login
        self.senha.data = usuario.senha
        self.role.data = usuario.role

class LoginForm(FlaskForm):
    login = StringField("Login:", validators=[DataRequired()])
    senha = PasswordField("Senha:", validators=[DataRequired()])


class DashboardGeralForm(FlaskForm):
    
    def calcular(self):
        self.total_alunos = Aluno.query.count()
        self.total_oficinas = Oficina.query.count()
        self.total_aulas = Aula.query.count()
        self.total_livros = Livro.query.count()

        self.total_alunos_masc = Aluno.query.filter_by(genero="masc").count()
        self.total_alunos_fem = Aluno.query.filter_by(genero="fem").count()

        self.oficinas = Oficina.query.all()
        