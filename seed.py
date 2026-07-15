from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(email="admin@gmail.com").first()
    if admin:
        print("Admin already exists")
    else:
        admin = User(
            name = "Admin", # type: ignore
            email = "admin@gmail.com", # type: ignore
            password = generate_password_hash("Admin@123"), # type: ignore
            role = "admin", # type: ignore
            approved = True, # type: ignore
            blacklisted = False # type: ignore
        )
        db.session.add(admin)
        db.session.commit()
        
        print("Admin created successfully")
        
    
        