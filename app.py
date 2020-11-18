from flask import Flask, escape, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import traceback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class My_post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(300), nullable=False)
    post_text = db.Column(db.Text, nullable=False)
    post_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.post_id

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        new_title = request.form['post_title']
        new_text = request.form['post_text']
        new_date = datetime.now()

        new_post = My_post(post_title=new_title, post_text=new_text, post_date=new_date)

        try:
            db.session.add(new_post)
            db.session.commit()
            return render_template('index.html', posts=get_posts())
        except:
            return traceback.format_exc()
    else:
        return render_template('index.html', posts=get_posts())

def get_posts():
    posts = My_post.query.order_by(My_post.post_date.desc()).all()
    if posts:
        for post in posts:
            post.post_date = datetime.strftime(post.post_date, '%d:%m:%Y %H:%M:%S') # чтобы время было в нужном формате
        return posts
    else:
        return 'Здесь ещё нет постов'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

