from app import create_app
from models import db, User

def create_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create default admin user
        admin_user = User(email="admin@example.com",
                          password_hash="admin",  # Not secure - for demo only
                          full_name="Admin User",
                          qualification="N/A",
                          role="admin")
        db.session.add(admin_user)
        db.session.commit()
        print("Database created and admin user added!")

if __name__ == "__main__":
    create_database()