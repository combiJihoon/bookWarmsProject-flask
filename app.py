from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect  # csrf

from db_connect import db
import config
import secrets


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    Migrate().init_app(app, db, render_as_batch=True)

    from views import main_view
    import model
    app.register_blueprint(main_view.bp)

    # 세션 암호화 => 서버가 정보를 암호화 해서 가지고 있겠다는 뜻
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == '__main__':
    create_app().run()
