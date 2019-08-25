from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.now().date())
    description = db.Column(db.String(250), unique=False)

    def __init__(self, name, title, date_created,  description):
        self.name = name
        self.title = title
        self.date_created = date_created
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.name


posts = [
    {
        'author': 'ashan p',
        'title': 'question 1',
        'content': 'Study for cmsc421',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'ligma',
        'title': 'question 2',
        'content': 'second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']

        description = request.form['description']

        p1 = Post(name, title, datetime.now().date(), description)

        try:
            db.session.add(p1)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding'
    else:
        post_list = Post.query.order_by(Post.date_created.desc()).all()
        return render_template('home.html', posts=post_list)


@app.route('/about')
def about():
    return render_template('about.html', title='about')


@app.route('/user')
def user():
    return render_template('about.html', title='about')


if __name__ == '__main__':
    app.run(debug=True)
