from database.connection import db
from database.models import User
from flask import Blueprint, request, redirect, url_for, session, render_template, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers.auth import *

bp = Blueprint('account', __name__, template_folder='../templates', url_prefix='/account')
bp.before_request(require_login)

@bp.route('/change_username', endpoint='change_username', methods=['GET', 'POST'])
def change_username():

    id = session['user_id']

    if request.method == 'POST':
        
        new_username = request.form.get('new_username')
        password = request.form.get('password')

        errors = []

        if not new_username or not password:
            errors.append('fill the fields')

        user_info = db.session.query(User).filter_by(id=id).first()

        if not check_password_hash(user_info.hashed_password, password):
            return 
        else:
            user_info.username = new_username
            db.session.commit()
            return redirect(url_for('account.configs'))

    else:
        return render_template('account/change_username.html', hide_header=True)

@bp.route('/change_password', endpoint='change_password', methods=['GET', 'POST'])
def change_password():

    id = session['user_id']

    if request.method == 'POST':
        
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        #Todo: Apology
        if not old_password or not new_password or not confirm_new_password:
            return 
        elif new_password != confirm_new_password:
            return 
        
        user_info = db.session.query(User).filter_by(id=id).first()

        if not user_info or not check_password_hash(user_info.hashed_password, old_password):
            return 
        
        new_hashed_password = generate_password_hash(new_password)

        user_info.hashed_password = new_hashed_password
        db.session.commit()

        return redirect(url_for('account.configs'))

    else:
        return render_template('account/change_password.html', hide_header=True)
    
@bp.route('/configs', endpoint='configs')
def configs():

    id = session['user_id']

    user = db.session.query(User).filter_by(id=id).first()

    return render_template('account/configs.html', user=user)
