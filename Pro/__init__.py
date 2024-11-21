from datetime import datetime,timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SECRETKEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.sqlite3'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    
    db.init_app(app)

    login_manager=LoginManager()
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        try:
            db.create_all()
            User.create_dummy_admin()
        except Exception as exception:
            print(exception)
    
    return app
