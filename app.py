from flask import Flask, render_template, flash, redirect, url_for, session, \
logging, request, jsonify
import random, string
from data import Articles, Categories
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField,validators
from passlib.hash import sha256_crypt
from appdb import *
from functools import wraps

# google plus
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('/var/www/catalog_app/client_secrets.json','r').read())['web']['client_id']

app = Flask(__name__, static_url_path='')

Articles = Articles()
categories = Categories()

@app.route('/')
@app.route('/home')
def home():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session['state'] = state
    print "the current state is %s"%session['state']
    return render_template('home.html', STATE=state)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/catalog/<string:id>')
def item(id):
    item = get_item(id)
    return render_template('item.html', item=item)

@app.route('/catalog/<string:category>/items')
def category(category):
    lowercase_category = category.lower()
    items_by_category = get_items_by_category(lowercase_category)
    return render_template('category.html', items=items_by_category, \
    categories=categories,the_category=category)

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
        print username
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

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:

        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # upgrade the authorization code into a credentials object
        print'works'
        oauth_flow = flow_from_clientsecrets('/var/www/catalog_app/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid
    access_token = credentials.access_token
    session['access_token'] = access_token
    print access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    print h
    http_request = h.request(url, 'GET')[1]
    print http_request
    result = json.loads(http_request)
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')),50)
        response.headers['Content-Type'] = 'application/json'
    gplus_id = credentials.id_token['sub']
    # Verify that the access token is used for the intended use
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dump("Token's user ID does not match given user ID."), 401
        )
        response.headers['Content-Type']= 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's"), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check to see if user is already logged in
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    # Store the access token in the session fot the later use.
    session['credentials'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token':credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params = params)

    data = answer.json()
    print data
    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    user_id = get_gplus_user_id(session['email'])
    if not user_id:
        user_id = add_gplus_user(session)
    session['user_id'] = user_id
    output = ' <h1>Welcome, {}!</h1><img src="{}" style = "width: 300px; border-radius: 150px;-moz-border-radius: 150px;">'.format(session['username'], session['picture'])
    flash("You are now logged in as {}".format(session['username']))
    return output

# disconnect based on provider
@app.route('/gdisconnect')
def gdisconnect():
    access_token = session['access_token']
    if access_token is None:
        response = make_response(json.dumps('Current user is not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    #Execute HTTP GET request to revoke current token.
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    print result
    if result['status'] == '200':
        # Reset the user's session.
        session.clear()
        print session
        flash('You are now logged out', 'success')
        return redirect(url_for('login'))
    else:
        # For whatever reason, the given token was invalid
        response = make_response(json.dumps('Failed to revoke for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session or session['access_token']:
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
    latest_items = get_latest_items()
    print latest_items
    print items
    if items > 0:
        return render_template('dashboard.html', items=items, categories=categories, \
        latest_items=latest_items)
    else:
        msg = 'No Items Found'
        return render_template('dashboard.html', msg=msg, categories=categories)

# Item Form class
class ItemForm(Form):
    title = StringField('Title', [validators.length(min=1, max=100)])
    category = SelectField('Category', choices=[('soccer','Soccer'),('basketball','Basketball'),('baseball','Baseball'),
    ('firsbee','Firsbee'),('snowboarding','Sonwboarding'),('rock_climbing','Rock Climbing'),
    ('foosball','Foosball'),('skating','Skating'),('hockey','Hockey')])
    description = TextAreaField('Description', [validators.length(min=30)])

# Add Item
@app.route('/catalog/add_item', methods=['GET', 'POST'])
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
@app.route('/catalog/edit_item/<string:id>', methods=['GET', 'POST'])
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
@app.route('/catalog/delete_item/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def delete_item(id):
    if request.method == 'POST':
        delete_item_from_db(id)
        flash('Item Deleted','success')
        return redirect(url_for('dashboard'))
    return render_template('delete_item.html')

@app.route('/catalog')
def catalog_json():
     if request.method == 'GET':
         raw_data = get_items()
         Category = []
         for data in raw_data:
             dic = {}
             dic['title'] = data['title']
             dic['category'] = data['category']
             dic['description'] = data['description'].replace('<p>', '').replace('</p>', '')
             Category.append(dic)
         print Category
         return jsonify(Category = Category)

if __name__ == "__main__":
    app.run()
