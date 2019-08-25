from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app1)

# il


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.now().date())
    description = db.Column(db.String(250), unique=False)
    phone = db.Column(db.String(12), unique=False, default="")
    email = db.Column(db.String(100), unique=False, default="")

    def __init__(self, name, title, date_created,  description, phone, email):
        self.name = name
        self.title = title
        self.date_created = date_created
        self.description = description
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


@app1.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        description = request.form['description']
        phone = request.form['phone']
        email = request.form['email']

        p1 = Post(name, title, datetime.now().date(),
                  description, phone, email)

        try:
            db.session.add(p1)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding'
    else:
        post_list = Post.query.order_by(Post.date_created.desc()).all()
        return render_template('home.html', posts=post_list)


@app1.route('/about')
def about():
    return render_template('about.html', title='about')


@app1.route('/<user_id>')
def user(user_id):
    person = Post.query.filter_by(id=user_id).first()
    return render_template('user.html', user=person)


@app1.route('/posts/<post_id>')
def post_comments(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('comment.html', post=post)


if __name__ == '__main__':
    app1.run(debug=True)
