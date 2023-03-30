from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pytz

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)

class todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' %self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = todo(content=task_content, date_created=datetime.utcnow() + timedelta(hours=5, minutes=30))

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding your task'

    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks=tasks)

    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    
    except:
        return 'There was a problem deleting that task!'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True)



# To initialize db, commands are:

# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()