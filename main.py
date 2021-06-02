from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET KEY'] = '7y90Rzj87kjl5t5r195rty'


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



@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template("register.html", title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
