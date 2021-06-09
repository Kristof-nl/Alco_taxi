from flask import render_template, flash, redirect, get_flashed_messages, url_for
from alco_taxi.models import User, Product, Order
from alco_taxi.forms import RegistrationForm, LoginForm
from alco_taxi import app, db, bcrypt


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/beer')
def beer():
    return render_template("beer.html")


@app.route('/wine')
def wine():
    return render_template("wine.html")


@app.route('/strong')
def strong():
    return render_template("strong.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #Hash password and put data to datebase
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}. You can login and start making orders.",'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"You have been logged in!",'success')
        return redirect(url_for('beer'))
    return render_template('login.html', title='Login', form=form)


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    return "basket"
