# Import Flask modules
from flask import Flask, redirect, url_for, render_template

# Create an object named app
app = Flask(__name__)

# Create a function named home
@app.route("/")
def home():
    return 'This is the home page for the root path, <h1>Welcome Home</h1>'

# Create a function named about
@app.route('/about')
def about():
    return '<h1>This is my about page</h1>'

# Create a function named error
@app.route('/error')
def error():
    return '<h1>Either you encountered an error or you are not authorized.</h1>'

# Create a function named admin
@app.route("/admin")
def admin():
    return redirect(url_for('error'))

# Create a function named greet
@app.route('/<name>')
def greet(name):
    return render_template('greet.html', name=name)

# Create a function named greet_admin
@app.route('/greet-admin')
def greet_admin():
    return redirect(url_for('greet', name='Master Admin!!!!'))

# Create a function named list10
@app.route('/list10')
def list10():
    return render_template('list10.html')

# Create a function named evens
@app.route('/evens')
def evens():
    return render_template('evens.html')

# Run the Flask application
if __name__== "__main__":
    app.run(host='0.0.0.0', port=80)


<!DOCTYPE html>
<html>
<head>
    <title>Greeting Page</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
    <h1>Welcome to my Greeting Page</h1>
</body>
</html>


<!DOCTYPE html>
<html>
<head>
    <title>List of Numbers</title>
</head>
<body>
    <h1>List of Numbers from 1 to 10</h1>
    <ul>
        {% for i in range(1, 11) %}
            <li>{{ i }}</li>
        {% endfor %}
    </ul>
</body>
</html>


<!DOCTYPE html>
<html>
<head>
    <title>List of Even Numbers</title>
</head>
<body>
    <h1>List of Even Numbers from 1 to 10</h1>
    <ul>
        {% for i in range(2, 11, 2) %}
            <li>{{ i }}</li>
        {% endfor %}
    </ul>
</body>
</html>
