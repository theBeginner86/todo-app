from datetime import datetime as dt

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # ///  ---> relative paths; //// ---> absolute paths
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime(), default=dt.now(), nullable=False)
    deadline = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_deadline = request.form['deadline']
        new_task = Todo(content=task_content, deadline=task_deadline)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "Ops!! We are facing some problem. Try back again."
    else:
        tasks = Todo.query.order_by(Todo.deadline).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_be_deleted = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_be_deleted)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was problem deleting. Please try again later!!'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_be_updated = Todo.query.get_or_404(id)

    if request.method == 'POST':
        try:
            task_to_be_updated.content = request.form['content']
            task_to_be_updated.deadline = request.form['deadline']

            db.session.commit()
            return redirect('/')
        except:
            return "Sorry, your task couldn't be updated at the moment"
    else:
        return render_template('update.html', task=task_to_be_updated)


if __name__ == "__main__":
    app.run(port=3111, host='0.0.0.0', debug=True)
