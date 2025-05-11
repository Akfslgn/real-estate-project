from app import create_app
from app.extensions import db

# Add confirmation for production environment


def reset_db():
    app = create_app('development')
    with app.app_context():
        confirm = input(
            "Are you sure you want to reset the database? This will delete all data. (yes/no): ")
        if confirm.lower() != "yes":
            print("Database reset aborted.")
            return
        print("Dropping all tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        print("Database reset complete!")


if __name__ == "__main__":
    reset_db()
