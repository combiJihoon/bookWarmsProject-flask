# 7/14 수요일 실습 강의 참고하기
from flask import Blueprint, render_template

board = Blueprint('board', __name__)


@board.route('/')
def home():
    return render_template('base.html')


@board.route('/post', methods=['GET'])
def post():
    return render_template('index.html')
