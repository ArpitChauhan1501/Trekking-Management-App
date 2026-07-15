from flask import Flask
from config import Config
from models import db, User
from flask_login import LoginManager
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.user import user_bp

app = Flask(__name__)

app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(user_bp)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login" #type:ignore

with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) 

if __name__ == '__main__':
    app.run(debug=True)