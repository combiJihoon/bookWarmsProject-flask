# 7/14 수요일 실습 강의 참고하기
from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from model import *
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return render_template('base.html')


@bp.route('/post', methods=['GET'])
def post():
    return render_template('index.html')


# 여기서부터 로그인
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        user_data = User.query.filter_by(id=user_id).first()

        if not user_data:
            flash('존재하지 않는 아이디입니다.')
            # user_id 다시 그대로 넘겨주기
            return redirect(url_for('main.login', user_id=user_id))

        elif not checkpw(user_pw.encode('utf-8'), user_data.user_pw):
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('main.login'))
        else:
            session.claer()

            session['user_id'] = user_id
            session['user_nickname'] = user_data.user_nickname

            flash(f'안녕하세요, {user_data.user_nickname}님!')
            return redirect(url_for('main.home'))
    else:
        return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@bp.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        user_id = reqeust.form['user_id']
        user = User.query.filter_by(id=user_id).first()
        # 등록된 사용자가 아닐 경우 가입 시작
        if not user:
            tmp_pw = request.form['user_pw']
            # 패스워드 해쉬
            user_pw = hashpw(tmp_pw.encode('utf-8'), gensalt())
            user_nickname = request.form['user_nickname']
            user_email = request.form['user_email']

            user = User(user_id=user_id, user_pw=user_pw,
                        user_nickname=user_nickname, user_email=user_email)

            db.session.add(user)
            db.session.commit()
        # 등록된 사용자일 경우 안내메시지
        else:
            flash('사용할 수 없는 아이디입니다.')
            return redirect(url_for('main.join'), user_id=user_id)
    else:
        return render_template('join.html')


# 여기서부터 회원가입
