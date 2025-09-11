from myshop import db,bcrypt,login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    budget=db.Column(db.Float,default=1000)
    books=db.relationship('Book',backref='owner',lazy=True)
    
    
    @property
    def password_hash(self):
        return self.password
    
    @password_hash.setter
    def password_hash(self,plain_text_password):
        self.password=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def correct_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password,attempted_password)
    
    @property
    def prettier_budget(self):
        if len(str(int(self.budget)))>=4:
            return f'{str(int(self.budget))[:-3]},{str(int(self.budget))[-3:]} $'
        else:
            return f'{int(self.budget)} $'


class Book(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    author=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Float,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    description=db.Column(db.Text,nullable=False)
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    @property
    def seller(self):
        if self.owner:
            return self.owner.username
        else:
            return 'No Owner'
    
    def buy(self,buyer,quantity):
        buyer.budget-=self.price
        self.quantity-=quantity
        if self.quantity==0:
            db.session.delete(self)
        self.owner.budget+=self.price*quantity
        db.session.commit()

    def __repr__(self):
        return f'Item {self.title}'

