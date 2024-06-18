from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token
from connectors.mysql_connector import engine

from sqlalchemy.orm import sessionmaker
import bcrypt
from models.user import User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route("/register", methods=['GET'])
def user_register():
    return render_template("users/register.html")

@user_routes.route("/register", methods=['POST'])
def do_registration():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()
    
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        flash('Email already registered')
        return redirect(url_for('user_routes.user_register'))

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    try:
        session.add(new_user)
        session.commit()
        flash('Registration successful. You can now log in.')
    except Exception as e:
        session.rollback()
        flash('Registration Failed')
        return redirect(url_for('user_routes.user_register'))
    
    return redirect(url_for('user_routes.user_login'))

@user_routes.route("/login", methods=['GET'])
def user_login():
    return render_template("users/login.html")

@user_routes.route("/login", methods=['POST'])
def do_user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        user = session.query(User).filter(User.email==email).first()

        # Check Email
        if not user:
            flash('Email not registered')
            return redirect(url_for('user_routes.user_login'))
        
        # Check Password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            flash('Wrong password')
            return redirect(url_for('user_routes.user_login'))

        login_user(user, remember=False)
        return redirect(url_for('account_routes.account_home'))

    except Exception as e:
        session.rollback()
        flash('Login Failed')
        return redirect(url_for('user_routes.user_login'))
    
@user_routes.route("/loginjwt", methods=['POST'])
def user_login_jwt():
    email = request.form.get('email')
    password = request.form.get('password')

    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    try:
        user = session.query(User).filter(User.email==email).first()

        # Check Email
        if not user:
            return jsonify({'message': 'Email not registered'})
        
        # Check Password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return jsonify({'message': 'Wrong password'})

        access_token = create_access_token(identity=user.id, additional_claims={"username": user.username})
        return jsonify({'access_token': access_token})

    except Exception as e:
        session.rollback()
        return jsonify({'message': e})
    
@user_routes.route("/logout", methods=['GET'])
def do_user_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('user_routes.user_login'))