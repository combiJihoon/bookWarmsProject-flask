from flask import Blueprint, render_template, url_for, request, session, flash, g
# from flask_wtf import csrf
from model import *
from werkzeug.utils import redirect
from bcrypt import hashpw, checkpw, gensalt

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET',))
def login_try():
    return render_template('login.html')


@bp.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']

    user_data = User.query.filter_by(user_id=user_id).first()

    if not user_data:
        flash("존재하지 않는 아이디입니다.")
        # user_id 다시 그대로 넘겨주기
        return redirect(url_for('auth.login_try'))

    elif not checkpw(user_pw.encode('utf-8'), user_data.user_pw):
        flash("비밀번호가 일치하지 않습니다.")
        return redirect(url_for('auth.login_try'))
    else:
        session.clear()

        session['user_id'] = user_id
        session['user_nickname'] = user_data.user_nickname

        flash(f'안녕하세요, {user_data.user_nickname}님!')
        return redirect(url_for('main.home'))


@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('로그아웃 되었습니다.')
    return redirect(url_for('main.home'))


@bp.route('/join', methods=['GET'])
def join():
    return render_template('join.html')


@bp.route('/join', methods=['POST'])
def register():
    user_id = request.form['user_id']
    tmp_pw = request.form['user_pw']

    user = User.query.filter_by(user_id=user_id).first()

    # 비밀번호 규칙 :8자리 이상(4자리 이상 문자 + 2자리 이상 숫자 + 2자리 이상 특수문자)
    check = [0] * len(tmp_pw)
    for i in range(len(tmp_pw)):
        if tmp_pw[i].isdigit():
            check[i] = 'digit'
        elif tmp_pw[i].isalpha():
            check[i] = 'alpha'
        else:
            check[i] = 'sign'
    if check.count('digit') < 2 or check.count('alpha') < 4 or check.count('sign') < 2:
        flash('비밀번호는 4자리 이상의 문자, 2자리 이상의 숫자, 2자리 이상의 특수문자가 포함되어야 합니다.')
        return redirect(url_for('auth.join'))

    # 등록된 사용자가 아닐 경우 가입 시작
    if not user:
        user_pw_check = request.form['user_pw_check']
        if len(tmp_pw) < 8:
            flash('비밀번호는 9자리 이상이어야 합니다.')
            return redirect(url_for('auth.join'))

        elif tmp_pw != user_pw_check:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for('auth.join'))

        # 패스워드 해쉬
        user_pw = hashpw(tmp_pw.encode('utf-8'), gensalt())
        user_name = request.form['user_name']
        user_nickname = request.form['user_nickname']
        user_email = request.form['user_email']

        user = User(user_id=user_id, user_pw=user_pw, user_name=user_name,
                    user_nickname=user_nickname, user_email=user_email)

        db.session.add(user)
        db.session.commit()
    # 등록된 사용자일 경우 안내메시지
    else:
        flash('사용할 수 없는 아이디입니다.')
        return "사용할 수 없는 아이디입니다."
    return redirect(url_for('main.home'))
