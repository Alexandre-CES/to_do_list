from flask import Flask, render_template, session
from flask_session import Session
from configs.config import Config
from helpers.auth import login_required
from database.models import *
from database.connection import db, Base, engine

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
Session(app)

Base.metadata.create_all(engine)

# Registrar os blueprints
from blueprints.account.account import bp as account_bp
from blueprints.friends.friends import bp as friends_bp
from blueprints.tasks.tasks import bp as tasks_bp
from blueprints.auth.auth import bp as auth_bp
app.register_blueprint(account_bp)
app.register_blueprint(friends_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)

@app.route('/', endpoint='index')
@login_required
def index():

    id = session['user_id']

    tasks = tasks = db.session.query(Task).filter_by(user_id=id).all()

    if tasks:
        for task in tasks:
            task.start = task.start.strftime('%d/%m/%y %H:%M')

            if task.ending:
                task.ending = task.ending.strftime('%d/%m/%y %H:%M')
            else:
                task.ending = ''


    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)