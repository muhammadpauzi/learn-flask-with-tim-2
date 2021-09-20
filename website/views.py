from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Post, User, Comment

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content = request.form.get('content').strip()

        if not content:
            flash('Post cannot be empty', category='error')
        else:
            new_post = Post(content=content, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

@views.route('/delete-post/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get(id)

    if not post:
        flash('Post does not exist.', category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted!', category='success')

    return redirect(url_for('views.home'))

@views.route('/<string:username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    return render_template('posts.html', user=current_user, posts=user.posts, username=user.username)

@views.route('/create-comment/<int:post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    content = request.form.get('content')

    if not content:
        flash('Comment cannot be empty', category='error')
    else:
        post = Post.query.get(post_id)

        if post:
            new_comment = Comment(content=content, author=current_user.id, post_id=post_id)
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
    
    return redirect(url_for('views.home'))

@views.route('/delete-comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted!.', category='success')
    
    return redirect(url_for('views.home'))