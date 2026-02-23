from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .auth import auth_bp
    from .trading import trading_bp
    from .portfolio import portfolio_bp
    from .dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(trading_bp, url_prefix="/trade")
    app.register_blueprint(portfolio_bp, url_prefix="/portfolio")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    with app.app_context():
        db.create_all()

    return app

