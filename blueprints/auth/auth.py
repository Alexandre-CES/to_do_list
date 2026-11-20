from database.connection import db
from database.models import User
from flask import Blueprint, request, redirect, url_for, session, render_template, session
from werkzeug.security import generate_password_hash
from helpers.auth import validate_auth_form, login_required

bp = Blueprint('auth', __name__, template_folder='../templates', url_prefix='/auth')

@bp.route('/register', endpoint='register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':

    form_data, errors = validate_auth_form(request.form.to_dict(), type='register')
    
    if len(errors) > 0:
        return redirect(url_for('auth.register', errors=errors))
    
    #geração de senha segura e insersão de conta na database
    hashed_password = generate_password_hash(form_data['password'])
    new_user = User(user=form_data['user'], username=form_data['username'], hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
  else:
    errors = request.args.getlist('errors')
    return render_template('auth/register.html', errors=errors, hide_header=True)

@bp.route('/login',endpoint='login', methods=['GET', 'POST'])
def login():
  session.clear()
  if request.method == 'POST':

    form_data, errors = validate_auth_form(request.form.to_dict(), type='login')

    if len(errors) > 0:
      return redirect(url_for('auth.login', errors=errors))
    session['user_id'] = form_data['id']
    return redirect(url_for('index'))
  
  else:
    errors = request.args.getlist('errors')
    return render_template('auth/login.html', errors=errors, hide_header=True)
       

@bp.route('/logout', endpoint='logout')
@login_required
def logout():
  session.clear()
  return redirect(url_for('auth.login'))