from database.connection import db
from flask import Blueprint,request
from helpers.helpers import *
from datetime import datetime
from database.models import *

bp = Blueprint('tasks', __name__)

@bp.route('/add_task', endpoint='add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':

        id = session['user_id']

        priority = request.form.get('priority')
        task = request.form.get('task')
        description = request.form.get('description')
        start = request.form.get('start')
        ending = request.form.get('ending')
        print(start)

        if not priority or not task:
            return apology('Precisa ter ao menos a tarefa e a prioridade(Se não tem prioridade você está provavelmente mechendo com o que não deve)', 403)
        if len(description) > 245 or len(task) > 42 or len(task) < 1:
            apology('como você digitou mais/menos que o permitido? está fazendo coisas ilícitas, rapaz?', 403)
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
