from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from apps.config import config

csrf = CSRFProtect()

# SOLAlchemyをインスタンス化する
db=SQLAlchemy()

# LoginManegerをインスタンス化する
login_maneger=LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定する
login_maneger.login_view = "auth.signup"
# login_messeage促成にログイン後に表示するメッセージを指定する
# ここでは指定しないように空を指定する
login_maneger.login_message = ""

# create_app関数を作成する
def create_app(config_key):
    # Flask インスタンス生成
    app = Flask(__name__)
    # アプリのコンフィグを設定する
    app.config.from_object(config[config_key])
    # app.config.from_mapping(
    #     SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
    #     SQLALCHEMY_DATABASE_URI=
    #      f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQLをコンソールログに出力する設定
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="AuxzyszU5sugKN7KZs6f" 
    # )

    csrf.init_app(app)

    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)
    # login_manegerをアプリケーションと連携する
    login_maneger.init_app(app)

    # crud パッケージからviewsをimportする
    from apps.crud import views as crud_views

    # register_blueprintを使いviewsのcrudをアプリへ登録する
    #app.register_blueprint(crud_views.crud, url_prefix="/crud")
    app.register_blueprint(crud_views.crud)

    # auth パッケージからviewsをimportする
    from apps.auth import views as auth_views

    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth") 

    # detectorパッケージからviewsをimportする
    from apps.detector import views as dt_views

    # register_blueprintを使いviewsのdtをアプリへ登録する
    #app.register_blueprint(dt_views.dt)
    app.register_blueprint(dt_views.dt, url_prefix="/detector") 

    from apps.iris import views as iris_views
    app.register_blueprint(iris_views.iris, url_prefix="/iris") 

    return app