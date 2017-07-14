from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField,validators
from passlib.hash import sha256_crypt
from appdb import add_user, get_user, add_item_to_db, get_items, get_item, update_item_to_db, delete_item_from_db
from functools import wraps

app = Flask(__name__)

Articles = Articles()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def item(id):
    item = get_item(id)
    return render_template('item.html', item=item)

# Register Form class
class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Use Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        add_user(name, email, username, password)
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])

# User Login
@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # Get Form Fields
        username = form.username.data
        password_candidate = form.password.data
        result = get_user(username, password_candidate)
        if result > 0:
            # Get stored hash
            password = result['password']
            print password
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] =True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Logging'
                app.logger.info('PASSWORD NOT MATCHED')
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are now logged out', )
            return redirect(url_for('login'))
    return wrap

# Log out
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    items = get_items()
    print items
    if items > 0:
        return render_template('dashboard.html', items=items)
    else:
        msg = 'No Items Found'
        return render_template('dashboard.html', msg=msg)

# Item Form class
class ItemForm(Form):
    title = StringField('Title', [validators.length(min=1, max=100)])
    category = SelectField('Category', choices=[('soccer','Soccer'),('basketball','Basketball'),('baseball','Baseball'),
    ('firsbee','Firsbee'),('snowboarding','Sonwboarding'),('rock climbing','Rock Climbing'),
    ('foosball','Foosball'),('skating','Skating'),('hockey','Hockey')])
    description = TextAreaField('Description', [validators.length(min=30)])

# Add Item
@app.route('/add_item', methods=['GET', 'POST'])
@is_logged_in
def add_item():
    form = ItemForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        category = form.category.data
        description = form.description.data

        # add item
        add_item_to_db(title, category, description)

        flash('Item Created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_item.html', form=form)

# Edit item
@app.route('/edit_item/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_item(id):
    item = get_item(id)
    form = ItemForm(request.form)
    # Populate article form fields
    form.title.data = item['title']
    form.category.data = item['category']
    form.description.data = item['description']
    if request.method == 'POST' and form.validate():
        print 'works'
        title = request.form['title']
        category = request.form['category']
        description = request.form['description']

        # update item
        update_item_to_db(id, title, category, description)

        flash('Item Updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_item.html', form=form)

# Delete item
@app.route('/delete_item/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_item(id):
    if request.method == 'POST':
        delete_item_from_db(id)
        flash('Item Deleted','success')
        return redirect(url_for('dashboard'))
    return render_template('delete_item.html')


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
