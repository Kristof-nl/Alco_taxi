from flask import render_template, flash, redirect, get_flashed_messages, url_for, request, session
from alco_taxi.models import User, Product, Order, Order_Item
from alco_taxi.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateItem, AddtoCart
from alco_taxi import app, db, bcrypt
from flask_login import login_user, current_user, logout_user
from alco_taxi.functions import get_user_name, handle_cart
import random

#Value to shown that cart is empty to avoid problems with session
empty_cart = True

#Route to get data from datebase
@app.context_processor
def context_processor():
    products = Product.query.all()
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
        flash(f"You don't have access to this section.",'danger')
        return render_template("home.html")


@app.route('/admin/product/')
def admin_product():
    if current_user.is_authenticated and current_user.username == 'admin':
        products = Product.query.all()
        return render_template("admin_product.html", title="Admin")
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")


@app.route('/admin/users/', methods=['GET', 'POST'])
def admin_users():
    if current_user.is_authenticated and current_user.username == 'admin':
        users = User.query.all()
        return render_template("admin_users.html", users=users)
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")


@app.route('/admin/users/delete<int:id>', methods=['GET', 'POST'])
def admin_delete_users(id):
    if current_user.is_authenticated and current_user.username == 'admin':
        user = User.query.get_or_404(id)
        if request.method == 'POST':
            if request.form.get('action1') == 'Delete':
                if user.username == "admin":
                    flash(f"You can't delete this user!!!",'danger')
                else:
                    db.session.delete(user)
                    db.session.commit()
                    flash(f"You have succesfully deleted user {user.username}.",'success')
                return redirect(url_for('admin_users'))
            else:
                return redirect(url_for('admin_users'))
        else:
            return render_template("delete.html", user=user)

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


@app.route('/admin/orders')
def admin_orders_list():
    if current_user.is_authenticated and current_user.username == 'admin':
       orders = Order.query.all()

       return render_template("admin_orders.html", orders=orders)
    else:
        flash(f"You don't have access to this section",'danger')
        return render_template("home.html")



@app.route('/admin/orders/<order_id>', methods=['GET','POST'])
def admin_orders(order_id):
    if current_user.is_authenticated and current_user.username == 'admin':
       order = Order.query.filter_by(id=int(order_id)).first()

       return render_template("admin_orders_summary.html", order=order)
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
    form = AddtoCart()

    return render_template("strong.html", form=form)


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    product = Product.query.filter_by(id=product_id).first()
    if product_id and quantity and request.method == "POST":
        session['cart'].append({'id': product_id, 'quantity': quantity})
        session.modified = True
        global empty_cart
        empty_cart = False
        flash(f'Product added to cart.', 'success')
    return redirect(url_for('cart'))


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
        return redirect(url_for('home'))
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


@app.route('/cart/')
def cart():
    if empty_cart == True:
        flash('Your cart is empty. Please add some products.', 'secondary')
        return redirect(url_for('home'))
    else:
        products, grand_total, grand_quantity, index = handle_cart()

        return render_template('cart.html', products=products, grand_total=grand_total, grand_quantity=grand_quantity)



@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    if not session['cart']:
        global empty_cart
        empty_cart = True
    return redirect(url_for('cart'))


@app.route('/checkout',  methods=['GET', 'POST'])
def checkout():
    first_name = request.form.get('first_name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    phone_number = request.form.get('phone')
    street = request.form.get('street')
    house_number = request.form.get('house')
    city = request.form.get('city')
    zip_code = request.form.get('zip')
    try:
        user = current_user.id
    except:
        user = 00
    
    products, grand_total, grand_quantity, index = handle_cart()

    if request.method == "POST":
    
        order = Order( first_name = request.form.get('first_name'), surname = request.form.get('surname'),
        email = request.form.get('email'), phone_number = request.form.get('phone'),  street = request.form.get('street'),
        house_number = request.form.get('house'), city = request.form.get('city'), area_code = request.form.get('zip'),
        reference = "".join([random.choice('ABCDEFGHIJK') for _ in range(8)]), status = "PENDING",
        customer_id = user)

        for product in products:
            order_item = Order_Item(quantity=product['quantity'], product_id=product['id'])
            order.items.append(order_item)

        db.session.add(order)
        db.session.commit()

        session['cart'] = []
        session.modified = True
        global empty_cart
        empty_cart = True
        flash(f'Thank you for your purchase. We will deliver your delivery as soon as posible.', 'success')
        return redirect(url_for('home'))

    return render_template('checkout.html', products=products, grand_quantity=grand_quantity, grand_total=grand_total)


@app.route('/account-menu')
def account_menu():
    if current_user.is_authenticated:
        user = current_user.id
        orders = Order.query.all()
    return render_template('account_menu.html', user=user, orders=orders)


@app.route('/account/<order_id>')
def account(order_id):
    order = Order.query.filter_by(id=int(order_id)).first()
    return render_template('account.html', order=order)



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html',title='Reset Password', form=form)
