from flask import render_template, redirect, session, request, flash, Flask
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login_or_reg')

@app.route('/login_or_reg')
def login_or_reg():
    users = User.get_all()
    return render_template('index.html', all_users = users)

@app.route('/login',  methods=["POST"])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')

    session['user_name'] = user_in_db.first_name
    session['user_id'] = user_in_db.id
    print('======================================', session['user_id'])
    return redirect('/home')

@app.route('/reg', methods=["POST"])
def reg():
    check = {'email' : request.form['email']}
    if not User.validate_user(request.form):
        return redirect('/')
    if  User.check_existing_email(check):
        flash('Email already registered', 'email')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    # user_id = User.save(data)
    # session['user_id'] = user_id
    return redirect('/')

@app.route('/home')
def home():
    if  not session.get("user_name"):
        return redirect('/')
    name = session['user_name']
    # id = session['user_id']
    recipes = Recipe.get_all_recipes()
    return render_template('home.html', name = name, all_recipes = recipes)

@app.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('user_id', None)
    return redirect('/')