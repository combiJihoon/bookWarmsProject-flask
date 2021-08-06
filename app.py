from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config
import secrets

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    Migrate().init_app(app, db)

    from views import main_view
    import model
    app.register_blueprint(main_view.board)

    # 세션 암호화 => 서버가 정보를 암호화 해서 가지고 있겠다는 뜻
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    app.config['SESSION_TYPE'] = 'filesystem'

    return app


if __name__ == '__main__':
    create_app().run()
