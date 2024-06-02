from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./email.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.before_first_request
def create_tables():
    db.create_all()
    users = [
        User(username='caner', email='caner@amazon.com'),
        User(username='hasan', email='hasan@google.com'),
        User(username='ibrahim', email='ibrahim@bmw.com'),
        User(username='ramazan', email='ramazan@mercedes.com'),
        User(username='aynur', email='aynur@porche.com'),
        User(username='fatih', email='fatih@huwaei.com'),
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_app_name = request.form['user_keyword']
        user_emails = User.query.filter(User.username.ilike(f'%{user_app_name}%')).all()
        if not user_emails:
            flash('No results found.')
        return render_template('emails.html', name_emails=user_emails, keyword=user_app_name, show_result=True)
    else:
        return render_template('emails.html', show_result=False)

@app.route('/add', methods=['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_app_name = request.form['username']
        user_app_email = request.form['useremail']
        if not user_app_name or not user_app_email:
            flash('Username or email can not be empty!!')
        else:
            user = User.query.filter_by(username=user_app_name).first()
            if user:
                flash(f'User {user_app_name} already exist')
            else:
                user = User(username=user_app_name, email=user_app_email)
                db.session.add(user)
                db.session.commit()
                flash(f"User {user_app_name} and {user_app_email} have been added successfully")
        return render_template('add-email.html', show_result=True)
    else:
        return render_template('add-email.html', show_result=False)

if __name__=='__main__':
    app.run(debug=True)
