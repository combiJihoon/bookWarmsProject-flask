from flask import Blueprint, render_template, url_for, request, session, flash, g
# from flask_wtf import csrf
from model import *
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('mypage', __name__, url_prefix='/mypage')


@bp.route('/posts', methods=['GET'])
def myposts():
    if session['user_id']:
        user_id = session['user_id']
        post_list = Post.query.filter_by(user_id=user_id).all()
        return render_template('mypage.html', post_list=post_list)
