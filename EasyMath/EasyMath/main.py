from flask import Flask,render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', error=None)

@app.route('/calculator')
def calculator():
    return render_template('calculator.html', error=None)

@app.route('/measurement')
def measurement():
    return render_template('measurement.html', error=None)


if __name__ == '__main__':
    app.run(debug=True)
