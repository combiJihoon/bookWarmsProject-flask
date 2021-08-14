# TODO 장르 카테고리, 책 제목 모델 추가하기, 책 API 가져오기
# TODO 다 읽은 것, 현재 진행형 카테고리 추가
# TODO <form id="signup" action="{{url_for('main.join')}}" method="post">{{form.csrf_token}} 해결하기
from flask import Blueprint, render_template, url_for, request, session, flash, g
# from flask_wtf import csrf
from model import *
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    post_list = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', post_list=post_list)
