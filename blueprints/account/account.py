from database.connection import db
from database.models import User
from flask import Blueprint, request, redirect, url_for, session, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from helpers.helpers import *

bp = Blueprint('account', __name__, template_folder='../templates')

@bp.route('/register', endpoint='register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form.get('username')
        user = request.form.get('user')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
            
        if not user or not password or not confirm_password:
            return apology('Preencha os campos vazios', 403)
        elif not username:
            username = user
        elif password != confirm_password:
            return apology('As senhas devem ser iguais', 403)
        
        if len(user) < 5 or len(user) > 20:
            return apology('usuário precisa ter no mínimo 5 e no máximo 20 dígitos', 403)
        elif len(password) < 10 or len(password) > 20:
            return apology('senha precisa ter no mínimo 10 e no máximo 20 dígitos', 403)
        
        repeat_user = db.session.query(User).filter_by(user=user).first()
        if repeat_user:
            return apology('Nome já está em uso', 403)

        #geração de senha segura e insersão de conta na database
        hashed_password = generate_password_hash(password)
        new_user = User(user=user, username=username, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('account.login'))
    else:
        return render_template('register.html', hide_header=True)


@bp.route('/login',endpoint='login', methods=['GET', 'POST'])
def login():

    session.clear()

    if request.method == 'POST':

        user = request.form.get('user')
        password = request.form.get('password')

        if not user or not password:
            return apology('Preencha os campos vazios', 403)
        
        user_info = User.query.filter_by(user=user).first()

        #checar se usuário existe e se a senha é correta
        if not user_info or not check_password_hash(user_info.hashed_password, password):
            return apology('Credenciais inválidas', 403)

        #acessar usuário que está logado
        session['user_id'] = user_info.id

        return redirect(url_for('index'))
    else:
        response = make_response(render_template('login.html', hide_header=True))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

@bp.route('/logout', endpoint='logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('account.login'))

@bp.route('/change_username', endpoint='change_username', methods=['GET', 'POST'])
@login_required
def change_username():

    id = session['user_id']

    if request.method == 'POST':
        
        new_username = request.form.get('new_username')
        password = request.form.get('password')

        if not new_username or not password:
            return apology('Preencha os todos os campos', 403)

        user_info = User.query.filter_by(id=id).first()

        if not check_password_hash(user_info.hashed_password, password):
            return apology('Credenciais inválidas', 403)
        else:
            user_info.username = new_username
            db.session.commit()
            return redirect(url_for('account.configs'))

    else:
        return render_template('change_username.html', hide_header=True)

@bp.route('/change_password', endpoint='change_password', methods=['GET', 'POST'])
@login_required
def change_password():

    id = session['user_id']

    if request.method == 'POST':
        
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        if not old_password or not new_password or not confirm_new_password:
            return apology('preencha os campos vazios', 403)
        elif new_password != confirm_new_password:
            return apology('a senha de confirmação e a nova senha estão diferentes', 403)
        
        user_info = User.query.filter_by(id=id).first()

        if not user_info or not check_password_hash(user_info.hashed_password, old_password):
            return apology('Credenciais inválias', 403)
        
        new_hashed_password = generate_password_hash(new_password)

        user_info.hashed_password = new_hashed_password
        db.session.commit()

        return redirect(url_for('account.configs'))

    else:
        return render_template('change_password.html', hide_header=True)
    
@bp.route('/configs', endpoint='configs')
@login_required
def configs():

    id = session['user_id']

    user = User.query.filter_by(id=id).first()

    return render_template('configs.html', user=user)
