from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'math'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your models (replace this with your actual models)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add your Exercise model fields here

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/calculator')
def calculator():
    return render_template('calculator.html', error=None)

@app.route('/measurement')
def measurement():
    return render_template('measurement.html', error=None)

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

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
