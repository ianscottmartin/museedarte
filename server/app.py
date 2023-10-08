from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Import your User model from models.py
from models import User

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username")
    password = request.json.get("password")

    # Check if the username is already taken
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    # Create a new user with the hashed password
    new_user = User(username=username, password_hash=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.authenticate(password):
        return jsonify({"message": "Invalid username or password"}), 401

    # Here, you can create a session or JWT token to keep the user logged in
    # For example, you can use Flask-Login or Flask-JWT-Extended for this purpose

    return jsonify({"message": "Login successful"}), 200

@app.route("/logout", methods=["POST"])
def logout():
    # Implement your logout logic here, based on your authentication mechanism
    # For example, if using Flask-JWT-Extended, you can revoke the token

    return jsonify({"message": "Logout successful"}), 200

if __name__ == '__main__':
    app.run(port=5000,debug=True)
