from flask import Flask, render_template, flash, redirect, get_flashed_messages, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '7y90Rzj87kjl5t5r195rty'
app.confiq['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullabe=False)
    email = db.Column(db.String(100), unique=True, nullabe=False)
    password = db.Column(db.String(60), nullabe=False)
    orders = db.relationship('Order', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), unique=True, nullabe=False)
    price = db.Column(db.Float(nullabe=False))
    barcode = db.Column(db.String(12), unique=True, nullabe=False)
    

    def __repr__(self):
        return f"Product('{self.product_name}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime, nullable=False, default=datetime.uctnow)
    items = db.relationship('Product', lazy=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Products in order('{self.items}')"


   


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


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    return "basket"


if __name__ == "__main__":
    app.run(debug=True)
