from wtforms import StringField,PasswordField,SubmitField,FloatField,IntegerField,TextAreaField,ValidationError,HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email,EqualTo,InputRequired
from myshop.models import User,Book

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=6,max=100)])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='Passwords must match')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class RechargeForm(FlaskForm):
    amount=FloatField('Amount',validators=[DataRequired()])
    submit=SubmitField('Recharge')

class OrderForm(FlaskForm):
    Buyer_id=StringField('Buyer',validators=[DataRequired()])
    Book_id=StringField('Book',validators=[DataRequired()])
    quantity=IntegerField('Quantity',validators=[InputRequired()])
    submit=SubmitField('🛒 Order Now!!')

    def validate_quantity(self,quantity):
        if quantity.data<=0:
            raise ValidationError('Quantity must be at least 1.') 
        book=Book.query.get(self.Book_id.data)
        if book is None:
            raise ValidationError('Book not found.')
        if book.quantity<quantity.data:
            raise ValidationError(f'Only these { book.quantity } copies are available')

class SellForm(FlaskForm):
    seller=StringField('Seller',validators=[DataRequired()])
    book_name=StringField('Book Name',validators=[DataRequired()])
    author_name=StringField('Author Name',validators=[DataRequired()])
    price=FloatField('price',validators=[InputRequired()])
    description=StringField('description',validators=[DataRequired()])
    quantity=IntegerField('quantity',validators=[InputRequired()])
    submit=SubmitField('Submit')
