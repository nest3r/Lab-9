from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель базы данных
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)

# Создание таблиц
with app.app_context():
    db.create_all()

# Маршруты
@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['POST'])
def add_project():
    title = request.form['title']
    link = request.form['link']
    new_project = Project(title=title, link=link)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear')
def clear_projects():
    db.session.query(Project).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
