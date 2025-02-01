import os

class Config:
    SECRET_KEY = 'una_clave_secreta_muy_segura'
    CSV_FILE_PATH = os.path.join(os.getcwd(), 'comments_backup.csv')