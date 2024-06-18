from flask import Blueprint, render_template, request, jsonify
from connectors.mysql_connector import Session
from models.transaction import Transaction
from models.account import Account
from flask_login import current_user, login_required

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route("/transaction", methods=['GET'])
@login_required
def transaction_home():
    try:
        session = Session()
        search_query = request.args.get('query', '')
        transactions = session.query(Transaction).filter(
            (Transaction.from_account_id == current_user.id) | (Transaction.to_account_id == current_user.id),
            (Transaction.description.ilike(f"%{search_query}%"))
        ).all()
        session.close()

        session = Session()
        accounts = session.query(Account).all()
        session.close()

        return render_template("transactions/transaction_home.html", transactions=transactions, response_data={'accounts': accounts})

    except Exception as e:
        print(e)
        return "Error Processing Data"

@transaction_routes.route("/transaction/<id>", methods=['GET'])
@login_required
def transaction_detail(id):
    try:
        session = Session()
        transaction = session.query(Transaction).filter(Transaction.id == id,
                                                        (Transaction.from_account_id == current_user.id) | (
                                                                Transaction.to_account_id == current_user.id)).first()
        session.close()
        if transaction:
            return render_template("transactions/transaction_detail.html", transaction=transaction)
        else:
            return "Data not found", 404

    except Exception as e:
        print(e)
        return "Error Processing Data", 500

@transaction_routes.route("/transaction", methods=['POST'])
@login_required
def transaction_insert():
    try:
        new_transaction = Transaction(
            from_account_id=current_user.id,
            to_account_id=request.form['to_account_id'],
            amount=request.form['amount'],
            description=request.form['description']
        )

        session = Session()
        session.add(new_transaction)
        session.commit()
        session.close()
        return jsonify(message="Success insert data"), 201

    except Exception as e:
        print(e)
        return jsonify(message="Fail to insert data"), 500

