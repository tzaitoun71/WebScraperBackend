import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a test model
class User(db.Model):
    __tablename__ = 'users'  # Define the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

# Ensure tables are created once when the app starts
@app.before_request
def create_tables():
    print("Creating tables if they do not exist...")
    db.create_all()

# Route to test the database connection and add a sample user
@app.get("/test-home")
def home():
    print("Home route accessed.")
    try:
        # Check if a user already exists
        if not db.session.query(User).first():
            print("No users found, adding a test user.")
            # Add a sample user to test
            test_user = User(name="Test User", email="testuser@example.com")
            db.session.add(test_user)
            db.session.commit()
            print("Test user added successfully.")
            return "Table created and test user added!"
        else:
            print("User already exists in the database.")
            return "Database is connected and table exists."
    except Exception as e:
        print("Error during user creation or database operation:", e)
        return "An error occurred. Check terminal for details."

if __name__ == "__main__":
    app.run(debug=True)
