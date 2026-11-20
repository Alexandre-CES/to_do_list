from flask import Blueprint,request, redirect, url_for, session, render_template
from database.connection import db
from database.models import *
from helpers.auth import *

bp = Blueprint('friends', __name__)

bp.before_request(require_login)

@bp.route('/friends', endpoint='friends')
def friends_f():

    id = session['user_id']

    friends = []
    
    user_friends = db.session.query(Friend).filter_by(user_id=id).all()

    for user_friend in user_friends:
        friend_info = db.session.query(User).filter_by(id=user_friend.friend_id).first()
        if friend_info:
            friends.append({'username':friend_info.username, 'user':friend_info.user, 'id':friend_info.id})

    return render_template('friends/friends.html', friends=friends)

#olhar tabela do amiguinho
@bp.route('/see_friend_tasks/<int:friend_id>', endpoint='see_friend_tasks')
def see_friend_task(friend_id):

    id = session['user_id']

    if not id:
        return redirect(url_for('/login'))

    is_friend = Friend.query.filter_by(user_id=id, friend_id=friend_id).first()
    if not is_friend:
        return 
    else:
        db.session.query(User).filter_by(id=id).all()
        friend_tasks = db.session.query(Task).filter_by(user_id=friend_id).all()

        friend_user = db.session.query(User).filter_by(id=friend_id).first()
        friend_username_info = friend_user.username

        if len(friend_username_info) > 10:
            friend_username = friend_username_info[:10]
        else:
            friend_username = friend_username_info        

        return render_template('friends/see_friend_tasks.html', friend_tasks=friend_tasks, friend_username=friend_username)

@bp.route('/add_friend', endpoint='add_friend', methods=['GET','POST'])
def add_friend():

    id = session['user_id']
 
    if request.method == 'POST':
        
        requested_id = request.form.get('requested_id')

        # Todo: apology
        if not requested_id:
            return 
        
        user_requested = db.session.query(User).filter_by(id=requested_id).first()
        friend_request = db.session.query(Request).filter_by(user_id=id, requested_id=requested_id).first()
        received_request = db.session.query(Request).filter_by(user_id=requested_id, requested_id=id).first()

        #no caso de não existir
        if not user_requested:
            return 
        elif int(requested_id) == int(id):
            return 
        #no caso de enviar mais de uma vez
        elif friend_request:
            return redirect(url_for('friends.add_friend'))
        #no caso de já ter recebido uma solicitação da pessoa que enviou
        elif received_request:
            already_friends = db.session.query(Friend).filter_by(user_id=id, friend_id=requested_id).first()
            if already_friends:
                return 
            else:
                db.session.delete(received_request)
                new_friend = Friend(user_id=id, friend_id=requested_id)
                db.session.add(new_friend)
                db.session.commit()
                new_friend = Friend(user_id=requested_id, friend_id=id)
                db.session.add(new_friend)
                db.session.commit()
        else:
            already_friends = db.session.query(Friend).filter_by(user_id=id, friend_id=requested_id).first()
            if already_friends:
                return 
            else:
                new_request = Request(user_id=id, requested_id=requested_id)
                db.session.add(new_request)
                db.session.commit()

        return redirect(url_for('friends.add_friend'))
    else:
        #tabela que contém usuários que enviaram pedido
        requests = []
        requests_ids = db.session.query(Request).filter_by(requested_id=id).all()
        for reques in requests_ids:
            user = db.session.query(User).filter_by(id=reques.user_id).first()
            if user:
                requests.append({'username':user.username, 'user': user.user, 'id':user.id})       

        return render_template('friends/add_friend.html', user_id=id, requests=requests)

#aceitar solicitação de amizade
@bp.route('/accept_friend_request/<int:request_id>', endpoint='accept_friend_request')
def accept_friend_request(request_id):

    id = session['user_id']

    request = db.session.query(Request).filter_by(user_id=request_id, requested_id=id).first()
    db.session.delete(request)
    db.session.commit()

    new_friend = Friend(user_id=id, friend_id=request_id)
    db.session.add(new_friend)
    db.session.commit()
    new_friend = Friend(user_id=request_id, friend_id=id)
    db.session.add(new_friend)
    db.session.commit()

    return redirect(url_for('friends.add_friend'))

#recusar solicitação de amizade
@bp.route('/reject_friend_request/<int:request_id>', endpoint='reject_friend_request')
def reject_friend_request(request_id):

    id = session['user_id']
    
    request = db.session.query(Request).filter_by(user_id=request_id, requested_id=id).first()
    db.session.delete(request)
    db.session.commit()
    return redirect(url_for('friends.add_friend'))