from flask import Blueprint, render_template, url_for, request, session, flash, g
# from flask_wtf import csrf
from model import *
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/post/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template('post_detail.html', post=post)


@bp.route('/create-post', methods=['POST'])
def create_post():
    content = request.form['content']
    title = request.form['title']
    # join 이용해 닉네임으로 고치기
    user_id = session['user_id']

    post = Post(user_id, title, content)

    db.session.add(post)
    db.session.commit()

    flash('성공적으로 작성 되었습니다!')
    return redirect(url_for('post.post_detail', post_id=post.id))


@bp.route('/create-post', methods=['GET'])
def create_try():
    return render_template('post_create.html')


@bp.route('/update-post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    content = request.form['content']
    title = request.form['title']

    post.title = title
    post.content = content

    db.session.commit()

    flash('성공적으로 수정 되었습니다!')
    return redirect(url_for('post.post_detail', post_id=post.id))


@bp.route('/update-post/<int:post_id>', methods=['GET'])
def update_try(post_id):
    post = Post.query.filter_by(id=post_id).first()

    return render_template('post_update.html', post=post)


@bp.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()

    flash('정상적으로 삭제 되었습니다.')
    return redirect(url_for('main.home'))
