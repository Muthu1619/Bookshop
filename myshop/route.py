from flask import render_template,flash,redirect,url_for
from myshop import app,db
from myshop.forms import RegistrationForm,LoginForm,RechargeForm,OrderForm,SellForm
from myshop.models import User,Book
from flask_login import login_user,logout_user,current_user

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data,password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', category='success')
        return redirect(url_for('login'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.correct_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.username}!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home'))

@app.route('/recharge',methods=['GET','POST'])
def recharge():
    form=RechargeForm()
    if form.validate_on_submit():
        if form.amount.data<=0 or form.amount.data>10000:
            flash('Please enter a valid amount to recharge.',category='danger')
            return redirect(url_for('recharge'))
        else:
            current_user.budget+=form.amount.data
            db.session.commit()
            flash(f'Your account has been recharged with {form.amount.data} $. Your new balance is {current_user.prettier_budget}.',category='success')
            return redirect(url_for('home'))
    return render_template('recharge.html',form=form)

@app.route('/buy',methods=['GET','POST'])
def buy():
    Books=Book.query.filter(Book.quantity!=0).all()
    form=OrderForm()
    if form.validate_on_submit():
        book=Book.query.get(form.Book_id.data)
        book.buy(User.query.get(form.Buyer_id.data),form.quantity.data)
        db.session.commit()
        flash(f'Order placed successfully for {form.quantity.data} copy/copies of the book.',category='success')
        return redirect(url_for('buy'))
    if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error in processing your order: {err_msg}', category='danger')
    return render_template('buy.html', Books=Books,form=form)

@app.route('/sell',methods=['GET','POST'])
def sell():
    form=SellForm()
    if form.validate_on_submit():
        book=Book(title=form.book_name.data,author=form.author_name.data,price=form.price.data,quantity=form.quantity.data,description=form.description.data,owner_id=form.seller.data)
        db.session.add(book)
        db.session.commit() 
        flash(f'Books were added for sale successfully.',category='success')
        return redirect(url_for('buy'))
    else:
        if form.errors != {}:
            for error_msg in form.errors.values():
                flash(f'There was an error in processing your request: {error_msg}', category='danger')
    return render_template('sell.html',form=form)

