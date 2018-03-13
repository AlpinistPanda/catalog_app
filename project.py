#!/usr/bin/env python2

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, User, CategoryItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print url
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/catalog/JSON')
def restaurantsJSON():
    categories = session.query(Category).all()

    main = {}
    main['categories'] = []
    for cat in categories:
        catDict = {}
        catDict['id'] = cat.id
        catDict['name'] = cat.name
        catDict['item'] = []
        catitems = session.query(CategoryItem).filter_by(
            category_id=cat.id).all()
        print len(catitems)
        for item in catitems:
            itemDict = {}
            print item.id
            itemDict['id'] = item.id
            itemDict['title'] = item.title
            itemDict['description'] = item.description
            print itemDict
            catDict['item'].append(itemDict)
        main['categories'].append(catDict)

    return jsonify(main)

# Show catalog


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).all()
    items = session.query(CategoryItem).limit(10)

    if 'username' not in login_session:
        return render_template(
            'publiccatalog.html', categories=categories, items=items)
    else:
        return render_template(
            'catalog.html', categories=categories, items=items)


# Show a category's items


@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items/')
def showItems(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(
        CategoryItem).filter_by(category_id=category.id).all()
    if 'username' not in login_session:
        return render_template(
            'publicitems.html', items=items,
            category=category, categories=categories)
    else:
        return render_template(
            'items.html', items=items,
            category=category, categories=categories)


# Create a new category item
# Everyone can create a new category item if they are logged in
@app.route('/catalog/items/new/', methods=['GET', 'POST'])
def newCategoryItem():
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':
        newCategoryItem = CategoryItem(
            title=request.form['title'],
            description=request.form['description'],
            category_id=request.form['category'], user_id=1)
        session.add(newCategoryItem)
        session.commit()
        return redirect(url_for(
            'showItems',
            category_name=categories[newCategoryItem.category_id-1].name))
    else:
        return render_template('newcategoryitem.html', categories=categories)


# Edit a Category item
# Only a person that created a category item can edit it
# authorization

@app.route(
    '/catalog/<category_name>/<item_title>/edit', methods=['GET', 'POST'])
def editCategoryItem(category_name, item_title):
    if 'username' not in login_session:
        return redirect('/login')

    editedItem = session.query(CategoryItem).filter_by(title=item_title).one()
    category = session.query(Category).filter_by(name=category_name).one()
    categories = session.query(Category).all()
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction() { " \
            "alert('You are not authorized to edit this category item" \
            " Please create your own category item." \
            " ');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template(
            'editcategoryitem.html', categories=categories,
            category_name=category_name, item_title=item_title,
            item=editedItem)

# View a Category item


@app.route('/catalog/<category_name>/<item_title>/')
def viewCategoryItem(category_name, item_title):
    item = session.query(CategoryItem).filter_by(title=item_title).one()
    category = session.query(Category).filter_by(name=category_name).one()

    if 'username' not in login_session:
        return render_template('publicview.html', item=item)
    else:
        return render_template('view.html', item=item)


# Delete a category item
# Only a person that created a category item can edit it

@app.route(
    '/catalog/<category_name>/<item_title>/delete', methods=['GET', 'POST'])
def deleteCategoryItem(category_name, item_title):
    if 'username' not in login_session:
        return redirect('/login')

    category = session.query(Category).filter_by(name=category_name).one()
    itemToDelete = session.query(
        CategoryItem).filter_by(title=item_title).one()
    if login_session['user_id'] != itemToDelete.user_id:
        return "<script>function myFunction() { " \
            "alert('You are not authorized to delete this category item" \
            " Please create your own category item." \
            " ');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItems', category_name=category_name))
    else:
        return render_template('deleteCategoryItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    gdisconnect()
    del login_session['gplus_id']
    del login_session['access_token']

    del login_session['username']
    del login_session['email']
    del login_session['user_id']

    return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
