from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required
from connectors.mysql_connector import Session
from models.account import Account

account_routes = Blueprint('account_routes', __name__)

@account_routes.route("/account", methods=['GET'])
@login_required
def account_home():
    try:
        session = Session()
        search_query = request.args.get('query', '')
        accounts = session.query(Account).filter(Account.user_id == current_user.id)\
                                          .filter(Account.account_number.ilike(f"%{search_query}%") |
                                                  Account.balance.ilike(f"%{search_query}%"))\
                                          .all()
        session.close()
        return render_template("accounts/account_home.html", response_data={'accounts': accounts, 'name': current_user.username})

    except Exception as e:
        print(e)
        return jsonify(message="Error processing data"), 500

@account_routes.route("/account/<id>", methods=['GET'])
@login_required
def account_detail(id):
    try:
        session = Session()
        account = session.query(Account).filter(Account.id == id, Account.user_id == current_user.id).first()
        session.close()
        if account:
            return render_template("accounts/account_detail.html", account=account)
        else:
            return jsonify(message="Data not found"), 404
        
    except Exception as e:
        print(e)
        return jsonify(message="Error processing data"), 500

@account_routes.route("/account", methods=['POST'])
@login_required
def account_insert():
    try:
        new_account = Account(
            user_id=current_user.id,
            account_number=request.form['accountNumber'],
            account_type=request.form['accountType'],
            balance=request.form['balance']
        )

        session = Session()
        session.add(new_account)
        session.commit()
        session.close()
        return jsonify(message="Success insert data"), 201
    
    except Exception as e:
        print(e)
        return jsonify(message="Fail to insert data"), 500

@account_routes.route("/account/<id>", methods=['DELETE'])
@login_required
def account_delete(id):
    try:
        session = Session()
        account = session.query(Account).filter(Account.id == id, Account.user_id == current_user.id).first()
        if account:
            session.delete(account)
            session.commit()
            session.close()
            return jsonify(message="Success delete data"), 200
        else:
            return jsonify(message="Data not found"), 404
        
    except Exception as e:
        print(e)
        return jsonify(message="Fail to delete data"), 500

@account_routes.route("/account/<id>", methods=['PUT'])
@login_required
def account_update(id):
    try:
        session = Session()
        account = session.query(Account).filter(Account.id == id, Account.user_id == current_user.id).first()
        if account:
            account.account_number = request.form['accountNumber']
            account.account_type = request.form['accountType']
            account.balance = float(request.form['balance'])
            session.commit()
            session.close()
            return jsonify(message="Success updating data"), 200
        else:
            return jsonify(message="Data not found"), 404
    
    except Exception as e:
        print(e)
        return jsonify(message="Fail to update data"), 500
