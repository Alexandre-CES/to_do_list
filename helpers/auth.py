from functools import wraps
from flask import redirect, url_for, session
from database.connection import db
from database.models import User
from werkzeug.security import check_password_hash

def require_login():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_auth_form(form_data: dict, type: str):
    errors = []

    id = None
    user = (form_data.get('user') or '').strip()
    username = (form_data.get('username') or user).strip()
    password = (form_data.get('password') or '').strip()
    confirm_password = (form_data.get('confirm_password') or '').strip()

    if not user or not password:
        errors.append('Preencha os campos')

    if len(user) < 5:
        errors.append('Usuário tem que ter, ao menos, 5 caracteres')
    
    if len(user) > 30:
        errors.append('Usuário pode ter, no máximo, 30 caracteres')

    if len(password) < 5:
        errors.append('Senha tem que ter, ao menos, 5 caracteres')

    if len(password) > 20:
        errors.append('Senha pode ter, no máximo, 20 caracteres')

    user_query = db.session.query(User).filter_by(user=user).first()

    if type == 'register':
        if user_query:
            errors.append('Usuário já existe')
        if password != confirm_password:
            errors.append('Senhas devem ser iguais')   
    elif type == 'login':
        #checar se usuário existe e se senha é correta
        if not user_query or not check_password_hash(user_query.hashed_password, password):
            errors.append('Credenciais incorretas')
        else:
            id = user_query.id

    return (
        {
            'id':id,
            'user' : user, 
            'username' : username,
            'password' : password, 
            'confirm_password' : confirm_password
        }, errors
    )