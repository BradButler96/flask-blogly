"""Blogly application."""
from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc, delete
from models import db, connect_db, User, Post, Tags, PostTags

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
def homepage():
    """Displays 5 most recent posts"""
    posts = Post.query.order_by(desc('posted_at')).limit(5)

    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Display custom 404"""

    return render_template('404.html'), 404

# users----------------------------------------------------------------------------------------------------------

@app.route('/users')
def show_all_users():
    """Display list of all users"""
    users = User.query.all()

    return render_template('users-all.html', users=users)


@app.route('/users/new')
def add_user():
    """Display add users page"""

    return render_template('user-add.html')


@app.route('/users/new', methods=['POST'])
def submit_add_user():
    """Submit add users page"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    profile_pic = request.form["profile_pic"]
    profile_pic = profile_pic if profile_pic else None

    new_user = User(first_name=first_name, last_name=last_name, profile_pic=profile_pic)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Display specified users page"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(posted_by=user_id)

    return render_template('user-page.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Display edit user page"""
    user = User.query.get_or_404(user_id)

    return render_template('user-edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edit_user(user_id):
    """Submit edit user page"""
    user = User.query.get_or_404(user_id)

    first_name = request.form["first_name"]
    user.first_name = first_name if first_name else user.first_name

    last_name = request.form["last_name"]
    user.last_name = last_name if last_name else user.last_name

    profile_pic = request.form["profile_pic"]
    user.profile_pic = profile_pic if profile_pic else user.profile_pic

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{ user.id }')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!')

    return redirect('/users')

# posts----------------------------------------------------------------------------------------------------------

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    """Display new post page"""
    user = User.query.get_or_404(user_id)
    tags = Tags.query.all()

    return render_template('post-add.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    """Submit new post page"""
    user = User.query.get_or_404(user_id)
    

    title = request.form['post_title']
    content = request.form['post_content']
    posted_by = user_id

    post = Post(title=title, content=content, posted_by=posted_by)

    db.session.add(post)
    db.session.commit()

    tag_names = request.form.getlist('tag-name')

    for tag in tag_names:
        new_tag = PostTags(post_id=post.id, tag_id=tag)
        db.session.add(new_tag)
    
    db.session.commit()

    return redirect(f'/users/{ user.id }')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Display post page"""
    post = Post.query.get(post_id)
    tags = PostTags.query.filter(PostTags.post_id == post_id)

    return render_template('post-page.html', post=post, tags=tags)
    

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Display edit post page"""
    post = Post.query.get_or_404(post_id)
    tags = Tags.query.all()

    return render_template('post-edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit_post(post_id):
    """Submit edit post page"""
    post = Post.query.get_or_404(post_id)

    title = request.form["edit_post_title"]
    post.title = title if title else post.title

    content = request.form["edit_post_content"]
    post.content = content if content else post.content

    tags = request.form.getlist('tags')

    post_tags = [int(tag) for tag in tags]
    post.tags = Tags.query.filter(Tags.id.in_(post_tags)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post page"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!')


    return redirect(f'/users/{ post.posted_by }')

# tags----------------------------------------------------------------------------------------------------------

@app.route('/tags')
def show_all_tags():
    """Display all tags"""
    tags = Tags.query.all()

    return render_template('tags-all.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Display specific tag details"""
    tag = Tags.query.get_or_404(tag_id)

    return render_template('tag-page.html', tag=tag)


@app.route('/tags/new')
def new_tag():
    """Display new tag page"""

    return render_template('tag-add.html')


@app.route('/tags/new', methods=['POST'])
def submit_new_tag():
    """Submit new tag page"""
    tag = request.form["tag_name"]
    new_tag = Tags(name=tag)
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Display specific tag details"""
    tag = Tags.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag-edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def submit_edit_tag(tag_id):
    """Submit specific tag details"""
    tag = Tags.query.get_or_404(tag_id)
    tag.name = request.form['tag_name']
    posts = request.form.getlist('posts')
    post_ids = [int(num) for num in posts]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect(f'/tags/{ tag_id }')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tags.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag has been deleted!')

    return redirect('/tags')



