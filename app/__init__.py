from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    username = 'uf1l9z4hpqcbr25b'
    password = 'PYglvYrNhJSmjvpKbGaz'
    hostname = 'blveriikn9teno6ow00e-mysql.services.clever-cloud.com'
    database = 'blveriikn9teno6ow00e'
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{hostname}/{database}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
    
    return app