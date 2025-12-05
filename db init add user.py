# test.py
from database.database import SessionLocal, init_db, Base, engine
from database.models import User
from auth.auth_utils import hash_password


def create_admin_user():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)  # 👈 force it here

    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == "admin").first()
    if existing_user:
        print("Admin user already exists.")
        db.close()
        return

    hashed_pw = hash_password("admin")
    admin_user = User(username="admin", hashed_password=hashed_pw)

    db.add(admin_user)
    db.commit()
    db.close()
    print("✅ Admin user created.")


if __name__ == "__main__":
    create_admin_user()
