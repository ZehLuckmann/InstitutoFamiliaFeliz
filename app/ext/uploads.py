import os
from config import UPLOAD_FOLDER

def configure(app):
    folder = f"{UPLOAD_FOLDER}/usuarios/fotos/"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    folder = f"{UPLOAD_FOLDER}/alunos/fotos/"
    if not os.path.exists(folder):
        os.makedirs(folder)