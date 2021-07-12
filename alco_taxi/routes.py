from flask import render_template, flash, redirect, get_flashed_messages, url_for, request
from alco_taxi.models import User, Product, Order
from alco_taxi.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateItem
from alco_taxi import app, db, bcrypt
from flask_login import login_user, current_user, logout_user
from alco_taxi.functions import get_user_name

#Route to get data from datebase
@app.context_processor
def context_processor():
    products = Product.query.all()
    print(products)
    return dict(products=products)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/admin/')
def admin():
    if current_user.is_authenticated and current_user.username == 'admin':
        products = Product.query.all()
        return render_template("admin.html", title="Admin")
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")


@app.route('/admin/product/')
def admin_product():
    if current_user.is_authenticated and current_user.username == 'admin':
        products = Product.query.all()
        return render_template("admin_product.html", title="Admin")
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")


@app.route('/admin/users/', methods="POST")
def admin_users():
    if current_user.is_authenticated and current_user.username == 'admin':
        users = User.query.all()
        if request.method=="POST":
            db.session.delete(user.id)
        return render_template("admin_users.html", users=users)
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")



@app.route('/admin/product/update<int:id>', methods=['GET','POST'])
def update(id):
    if current_user.is_authenticated and current_user.username == 'admin':
        product = Product.query.get_or_404(id)
        form = UpdateItem()
        if form.validate_on_submit():
            product.product_name = form.product_name.data
            product.price = form.product_price.data
            product.barcode = form.barcode.data
            product.image = form.image.data
            db.session.commit()
            flash(f"You product has been updated",'success')
            return redirect(url_for('admin_product'))

        form.product_name.data = product.product_name
        form.product_price.data = product.price
        form.barcode.data = product.barcode
        form.image.data = product.image
        

        return render_template("update.html", title="Update item", form=form, product=product)
    else:
        flash(f"You don't have access to this section",'danger')
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
    #Get user to home page if he is log already in
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
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
    #Get user to home page if he is log already in
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = LoginForm()
    form2 = RegistrationForm()
    if form.validate_on_submit():
        #User validation
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            if current_user.username == 'admin':
                flash(f'Welcome admin!', 'success')
            else:
                flash(f'Welcome {get_user_name(user)}! You can start making orders.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/cart')
def basket():
    return "cart"

@app.route('/account')
def account():
    return "account"


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html',title='Reset Password', form=form)
