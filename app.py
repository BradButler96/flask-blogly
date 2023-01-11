"""Blogly application."""
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'HendrixIsAnnoying123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def user_list():
    users = User.query.all()

    return render_template('home.html', users=users)



# @app.route('/', methods=["POST"])
# def create_user():
    # first_name = request.form["first_name"]
    # last_name = request.form["last_name"]
    # profile_pic = request.form["profile_pic"]
    # profile_pic = profile_pic if profile_pic else None

    # new_user = User(first_name=first_name, last_name=last_name, profile_pic=profile_pic)
    # db.session.add(new_user)
    # db.session.commit()

#     return redirect(f"/{new_user.id}")



@app.route('/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)



@app.route('/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('user.html', user=user) 



@app.route('/<int:user_id>', methods=["POST"])
def save_user(user_id):
    user = User.query.get_or_404(user_id)

    first_name = request.form["edit_first_name"]
    user.first_name = first_name if first_name else user.first_name

    last_name = request.form["edit_last_name"]
    user.last_name = last_name if last_name else user.last_name

    profile_pic = request.form["edit_profile_pic"]
    user.profile_pic = profile_pic if profile_pic else user.profile_pic

    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")



@app.route('/add')
def add_user_info():

    return render_template('add.html')



@app.route('/add/user', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    profile_pic = request.form["profile_pic"]
    profile_pic = profile_pic if profile_pic else None

    new_user = User(first_name=first_name, last_name=last_name, profile_pic=profile_pic)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/{new_user.id}")



@app.route('/<int:user_id>/delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
