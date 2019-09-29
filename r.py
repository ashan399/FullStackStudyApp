from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

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
    going = db.Column(db.Integer, unique=False, default=0)
    comments = db.Column(db.String(1000), unique=False, default="")

    def __init__(self, name, title, date_created,  description, phone, email, going, comments):
        self.name = name
        self.title = title
        self.date_created = date_created
        self.description = description
        self.phone = phone
        self.email = email
        self.going = going
        self.comments = comments

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        description = request.form['description']
        phone = request.form['phone']
        email = request.form['email']

        p1 = Post(name, title, datetime.now().date(),
                  description, phone, email, 0, "")

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


@app.route('/<user_id>')
def user(user_id):
    person = Post.query.filter_by(id=user_id).first()
    return render_template('user.html', user=person)


@app.route('/posts/<post_id>', methods=['POST', 'GET'])
def post_comments(post_id):

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date = str(datetime.now())[0:-10]
        post = Post.query.filter_by(id=post_id).first()
        post.comments += '⠀⠀⠀' + description + ' - ' + \
            name + ', ' + date + '\n\n'
        db.session.commit()
        return render_template('comment.html', post=post)
    else:
        post = Post.query.filter_by(id=post_id).first()
        return render_template('comment.html', post=post)


@app.route('/going/<post_id>')
def going(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.going += 1
    db.session.commit()
    return redirect('/')


@app.route('/cancelgoing/<post_id>')
def cancel_going(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post.going -= 1
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
