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
    order = db.Column(db.Integer(), db.ForeignKey('order.id'))

    def __repr__(self):
        return f"Product('{self.product_name}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_time = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    items = db.relationship('Product', lazy=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Products in order('{self.items}')"