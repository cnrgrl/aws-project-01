import os
import boto3
from botocore.exceptions import ClientError
from flask import Flask, render_template, request, flash
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Retrieve secrets from AWS Secrets Manager
def get_secret():
    secret_name = os.environ.get("SECRET_NAME")
    region_name = os.environ.get("REGION_NAME")

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Parse the secret string as JSON
    secret = json.loads(get_secret_value_response['SecretString'])
    
    return secret

secrets = get_secret()

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = secrets['host']
app.config['MYSQL_DATABASE_USER'] = secrets['username']
app.config['MYSQL_DATABASE_PASSWORD'] = secrets['password']
app.config['MYSQL_DATABASE_DB'] = secrets['dbname']
app.config['MYSQL_DATABASE_PORT'] = secrets['port']
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()

# Create users table within MySQL db and populate with sample data
# Execute the code below only once.
# Write sql code for initializing users table..
drop_table = 'DROP TABLE IF EXISTS users;'
users_table = """
CREATE TABLE users (
  username varchar(50) NOT NULL,
  email varchar(50),
  PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
data = """
INSERT INTO clarusway.users 
VALUES 
    ("caner", "caner@amazon.com"),
    ("hasan", "hasan@google.com"),
    ("ibrahim", "ibrahim@bmw.com"),
    ("ramazan", "ramazan@mercedes.com"),
	("aynur", "aynur@porche.com"),
    ("fatih", "fatih@huwaei.com");
"""
cursor = connection.cursor()
cursor.execute(drop_table)
cursor.execute(users_table)
cursor.execute(data)
connection.commit()

# Write a function named `find_emails` which find emails using keyword from the user table in the db,
# and returns result as tuples `(name, email)`.

def find_emails(keyword):
    query = "SELECT * FROM users WHERE username LIKE %s;"
    cursor.execute(query, ('%' + keyword + '%',))
    result = cursor.fetchall()
    user_emails = [(row[0], row[1]) for row in result]
    # if there is no user with given name in the db, then give warning
    if not any(user_emails):
        user_emails = [('Not found.', 'Not Found.')]
    return user_emails

# Write a function named `insert_email` which adds new email to users table the db.
def insert_email(name, email):
    query = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(query, (name,))
    result = cursor.fetchall()
    # default text
    response = ''
    # if user input are None (null) give warning
    if len(name) == 0 or len(email) == 0:
        flash('Username or email can not be empty!!')
    # if there is no same user name in the db, then insert the new one
    elif not any(result):
        insert = "INSERT INTO users (username, email) VALUES (%s, %s);"
        cursor.execute(insert, (name, email))
        connection.commit()
        response = f'User {name} and {email} have been added successfully'
    # if there is user with same name, then give warning
    else:
        flash(f'User {name} already exits.')
    return response

# Write a function named `emails`
@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_name = request.form['user_keyword']
        user_emails = find_emails(user_name)
        return render_template('emails.html', name_emails=user_emails, keyword=user_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)

# Write a function named `add_email`
@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['useremail']
        result = insert_email(user_name, user_email)
        return render_template('add-email.html', result_html=result, show_result=True)
    else:
        return render_template('add-email.html', show_result=False)

# Add a statement to run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
