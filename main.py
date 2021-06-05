from flask import Flask, render_template, flash, redirect, get_flashed_messages, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '7y90Rzj87kjl5t5r195rty'


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
        flash(f"Account created for {form.username.data}. You can start making orders.",'success')
        return redirect(url_for('beer'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"You have been logged in!",'success')
        return redirect(url_for('beer'))
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
