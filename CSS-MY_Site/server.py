from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-records.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Account(db.Model):
    name = db.Column(db.String(250), nullable=False)
    mobile = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(250), unique=True, nullable=False)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("password")
        user = Account.query.filter_by(mail=email, password=password).first()
        if not user:
            return redirect(url_for('Signup'))
        else:
            return redirect(url_for('home'))
    return render_template("login.html")


@app.route('/signup', methods=["GET", "POST"])
def Signup():
    if request.method == "POST":
        new_account = Account(
            name=request.form['name'],
            mobile=request.form['mobile'],
            mail=request.form['mail'],
            password=request.form['password']

        )
        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("signup.html")


@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/hobbies')
def hobbies():
    return render_template("my_hobbies.html")


if __name__ == "__main__":
    app.run(debug=True)
