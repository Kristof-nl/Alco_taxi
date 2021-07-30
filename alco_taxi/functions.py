from flask import flash, session
from alco_taxi.models import Product

#Function to get user_name when we log in
def get_user_name(user):
    user_name = str(user)[6:]
    end = int(user_name.find("'"))
    return user_name[:end]

#Function to calculate products in cart
def handle_cart():
    products = []
    grand_total = 0
    grand_quantity = 0
    index = 0
    for item in session['cart']:

        product = Product.query.filter_by(id=item['id']).first()

        quantity = int(item['quantity'])
        total = quantity * product.price
        grand_total += total
        grand_quantity += quantity

        products.append({'id': product.id, 'name': product.product_name, 'price': product.price, 'image': product.image,
        "quantity": quantity, 'total': total, 'index': index})

        index += 1

        if not products:
            flash('Your cart is empty. Please add some product.', 'secondary')
            return redirect(url_for('home'))

    return products, grand_total, grand_quantity, index

