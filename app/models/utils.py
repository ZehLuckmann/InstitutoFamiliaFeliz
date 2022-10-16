from datetime import timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

#Constantes
DIAS_SEMANA = [
    ("0", "Segunda-Feira"),
    ("1", "Terça-Feira"), 
    ("2", "Quarta-Feira"), 
    ("3", "Quinta-Feira"), 
    ("4", "Sexta-Feira"), 
    ("5", "Sábado"), 
    ("6", "Domingo")]

ROLES = [
    ("admin", "Administrador"),
    ("coordenador", "Coordenador"), 
    ("responsavel", "Responsavel"), ]

CSS_CLASS_FIELD = "form-control"