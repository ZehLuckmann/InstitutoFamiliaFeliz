from datetime import timedelta, datetime

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def inicio_semestre_atual():
    return datetime(datetime.now().year, 1, 1) if datetime.now().month <=6 else datetime(datetime.now().year, 7, 1)

def fim_semestre_atual():
    return datetime(datetime.now().year, 6, 30) if datetime.now().month <=6 else datetime(datetime.now().year, 12, 31)

#Constantes
DIAS_SEMANA = [
    ("0", "Segunda-Feira"),
    ("1", "Terça-Feira"), 
    ("2", "Quarta-Feira"), 
    ("3", "Quinta-Feira"), 
    ("4", "Sexta-Feira"), 
    ("5", "Sábado"), 
    ("6", "Domingo")]

GENERO = [
    ("masc", "Masculino"),
    ("fem", "Feminino"), 
    ("out", "Outro"), ]

ROLES = [
    ("coordenador", "Coordenador"), 
    ("responsavel", "Responsavel"), ]

CSS_CLASS_FIELD = "form-control"