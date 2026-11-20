from database.connection import db
from flask import Blueprint, request, session, redirect, render_template,url_for
from helpers.auth import require_login
from datetime import datetime
from database.models import Task

bp = Blueprint('tasks', __name__)

bp.before_request(require_login)

@bp.route('/add_task', endpoint='add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':

        id = session['user_id']

        priority = request.form.get('priority')
        task = request.form.get('task')
        description = request.form.get('description')
        start = request.form.get('start')
        ending = request.form.get('ending')

        # TODO: Apology
        if not priority or not task:
            return
        if len(description) > 245 or len(task) > 42 or len(task) < 1:
            return
        if start:
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        else:                           
            start = datetime.now().strftime('%Y-%m-%dT%H:%M')
            start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        if ending:
            ending = datetime.strptime(ending, '%Y-%m-%dT%H:%M')
        else:
            ending = None    

        new_task = Task(user_id=id, priority=priority, task=task, description=description, start=start, ending=ending)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index'))
        

    else:
        priorities = [0,1,2,3]
        return render_template('add_task.html', priorities=priorities)
