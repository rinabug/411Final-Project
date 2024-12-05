import os
import hashlib
import uuid
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database setup
DB_PATH = os.getenv('DB_PATH', 'sqlite:///users.db')
engine = create_engine('DB_PATH', echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# User model
class User(Base):
    __tablename__ = 'users_cli'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    salt = Column(String(64), nullable=False)
    password_hash = Column(String(128), nullable=False)

# Create tables
Base.metadata.create_all(engine)

def hash_password(password, salt):
    """Hash a password with the given salt."""
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000
    )
    return pwdhash.hex()

def create_account():
    username = input("Enter new username: ")
    password = input("Enter new password: ")

    # Check if username already exists
    if session.query(User).filter_by(username=username).first():
        print("Username already exists.")
        return

    salt = uuid.uuid4().hex
    password_hash = hash_password(password, salt)

    new_user = User(username=username, salt=salt, password_hash=password_hash)
    session.add(new_user)
    session.commit()

    print("Account created successfully.")

def login():
    username = input("Enter username: ")
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("Invalid username.")
        return
    password = input("Enter password: ")


    password_hash = hash_password(password, user.salt)
    if password_hash != user.password_hash:
        print("Invalid username or password.")
        return

    print("Login successful.")

def update_password():
    username = input("Enter username: ")
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print("Invalid username.")
        return
    
    old_password = input("Enter current password: ")
    old_password_hash = hash_password(old_password, user.salt)
    if old_password_hash != user.password_hash:
        print("Invalid current password.")
        return

    new_password = input("Enter new password: ")



    new_salt = uuid.uuid4().hex
    new_password_hash = hash_password(new_password, new_salt)

    user.salt = new_salt
    user.password_hash = new_password_hash
    session.commit()

    print("Password updated successfully.")

def main():
    while True:
        print("\nPlease choose an option:")
        print("1. Create Account")
        print("2. Login")
        print("3. Update Password")
        print("4. Exit")
        choice = input("Enter choice (1-4): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            update_password()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
