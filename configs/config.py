
from tempfile import mkdtemp

class Config:
    TEMPLATES_AUTO_RELOAD = True,
    SESSION_FILE_DIR = mkdtemp() #salvar sessão no arquivo temp
    SESSION_PERMANENT = False 
    SESSION_TYPE = 'filesystem' #sessão será guardada em algum arquivo
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tdl.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False