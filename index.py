from dotenv import load_dotenv
from flask import Flask, render_template
from connectors.mysql_connector import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from models.account import Account
from models.user import User
import os

# Load Controller Files
from controllers.account import account_routes
from controllers.user import user_routes
from controllers.transaction import transaction_routes

load_dotenv()

app=Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

jwt = JWTManager(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))

app.register_blueprint(user_routes)
app.register_blueprint(account_routes)
app.register_blueprint(transaction_routes)

# Account Route
@app.route("/")
def hello_world():
    connection = engine.connect()
    account_query = select(Account)
    Session = sessionmaker(connection)
    with Session() as session:
        result = session.execute(account_query)
        for row in result.scalars():
            print(f'ID: {row.id}, Name: {row.account_type}')

    return render_template("users/login.html")

if __name__ == "__main__":
    app.run(debug=True)