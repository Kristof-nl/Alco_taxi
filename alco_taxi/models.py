import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from alco_taxi import db, login_manager, app
from flask_login import UserMixin


#Function to load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Create models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Reset password with token
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumb({'user_id': seld.id}).decode('utf-8')

    @ staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float)
    barcode = db.Column(db.String(12), unique=True, nullable=False)
    image = db.Column(db.String(50), unique=True, nullable=False)


    def __repr__(self):
        return f"Product('{self.product_name}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    reference = db.Column(db.String(10))
    first_name = db.Column(db.String(25))
    surname = db.Column(db.String(25))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    street = db.Column(db.String(50))
    house_number = db.Column(db.String(10))
    city = db.Column(db.String(50))
    area_code = db.Column(db.String(10))
    status = db.Column(db.String(10))
    items = db.relationship('Order_Item', backref='order', lazy=True)

    def order_total(self):
        return db.session.query(db.func.sum(Order_Item.quantity * Product.price)).join(Product).filter(Order_Item.order_id == self.id).scalar()

    def order_quantity(self):
        return db.session.query(db.func.sum(Order_Item.quantity)).join(Product).filter(Order_Item.order_id == self.id).scalar()


 
class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
