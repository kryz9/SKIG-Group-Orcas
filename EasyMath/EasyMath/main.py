import secrets

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'math'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models (replace this with your actual models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add your Exercise model fields here

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)

# Set the secret key for the application using the app.secret_key attribute
app.secret_key = secrets.token_hex(16)

# Alternatively, you can set the secret key using the app.config['SECRET_KEY'] dictionary
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Set up an application context with app.app_context()
with app.app_context():
  # Create the database tables by calling the db.create_all() method
  db.create_all()

# Define a function that checks if the user is logged in
def is_logged_in():
  return 'user_id' in session

# Define a function that gets the current user object
def get_current_user():
  if is_logged_in():
    return User.query.get(session['user_id'])


#ROUTING PART
# Define the route for the landing page
@app.route('/')
def index():
  return render_template('landing-page.html')

# Define the route for the sign up page
# Define the route for the sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  # If the user is already logged in, redirect to the main page
  if is_logged_in():
    return redirect(url_for('main'))

  # If the request method is POST, get the form data and validate it
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    # Check if the name, email, and password are not empty
    if not name or not email or not password:
      return render_template('sign-up.html', message='Please fill in all the fields.')

    # Check if the password and confirm password match
    if password != confirm:
      return render_template('sign-up.html', message='Passwords do not match.')

    # Check if the email already exists in the database
    user = User.query.filter_by(email=email).first()
    if user:
      return render_template('sign-up.html', message='Email already registered.')

    # Create a new user object with the hashed password
    user = User(name=name, email=email, password=generate_password_hash(password))

    # Add the user to the database and commit the changes
    db.session.add(user)
    db.session.commit()

    # Store the user id in the session and redirect to the main page
    session['user_id'] = user.id
    return redirect(url_for('main'))

  # If the request method is GET, render the sign up template
  return render_template('sign-up.html')

# Define the route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  # If the user is already logged in, redirect to the main page
  if is_logged_in():
    return redirect(url_for('main'))

  # If the request method is POST, get the form data and validate it
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email and password are not empty
    if not email or not password:
      return render_template('login.html', message='Please fill in all the fields.')

    # Check if the email exists in the database
    user = User.query.filter_by(email=email).first()
    if not user:
      return render_template('login.html', message='Invalid email or password.')

    # Check if the password matches the hashed password in the database
    if not check_password_hash(user.password, password):
      return render_template('login.html', message='Invalid email or password.')

    # Store the user id in the session and redirect to the main page
    session['user_id'] = user.id
    return redirect(url_for('main'))

  # If the request method is GET, render the login template
  return render_template('login.html')

# Define the route for the logout function
@app.route('/logout')
def logout():
  # Remove the user id from the session and redirect to the landing page
  session.pop('user_id', None)
  return redirect(url_for('index'))

# Define the route for the main page
@app.route('/main')
def main():
  # If the user is not logged in, redirect to the login page
  if not is_logged_in():
    return redirect(url_for('login'))

  # Get the current user object and render the main template with the user data
  user = get_current_user()
  return render_template('index.html', user=user, error=None)

@app.route('/calculator')
def calculator():
  # If the user is not logged in, redirect to the login page
  if not is_logged_in():
    return redirect(url_for('login'))

  # Get the current user object and render the main template with the user data
  user = get_current_user()
  return render_template('calculator.html', user=user, error=None)

@app.route('/measurement')
def measurement():
  # If the user is not logged in, redirect to the login page
  if not is_logged_in():
    return redirect(url_for('login'))

  # Get the current user object and render the main template with the user data
  user = get_current_user()
  return render_template('measurement.html', user=user, error=None)

@app.route('/exercisealgebraeasy1')
def exercisealgebraeasy1():
    return render_template('exercisealgebraeasy1.html', error=None)

@app.route('/exercisealgebraeasy2')
def exercisealgebraeasy2():
    return render_template('exercisealgebraeasy2.html', error=None)

@app.route('/exercisealgebraeasy3')
def exercisealgebraeasy3():
    return render_template('exercisealgebraeasy3.html', error=None)

@app.route('/save_progress', methods=['POST'])
def save_progress():
    # Assuming your form has fields: user_id, exercise_id, is_correct
    user_id = request.form.get('user_id')
    exercise_id = request.form.get('exercise_id')
    is_correct = request.form.get('is_correct')

    # Create a UserProgress instance and add it to the database
    progress = UserProgress(user_id=user_id, exercise_id=exercise_id, is_correct=is_correct)
    db.session.add(progress)
    db.session.commit()

    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
