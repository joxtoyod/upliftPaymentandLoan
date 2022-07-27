from flask import Flask
from flask_migrate import Migrate
from models import models
from schemas import validators
from services import transactions, ledger
from config.db import DATABASE_CONNECTION_URI
from flask_pydantic import validate

def create_app():
    """Initializes and configures the application"""
    flask_app = Flask(__name__)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.app_context().push()

    models.db.init_app(flask_app)
    Migrate(flask_app, models.db)
    models.db.create_all()

    return flask_app

app = create_app()


@app.route('/account/create', methods=["POST"])
@validate()
def create_account(body: validators.PydanticAccountRequest):
    account = models.Account(**body.__dict__)
    models.db.session.add(account)
    models.db.session.commit()
    account = models.Account.query.get(account.id)
    return models.PydanticAccount.from_orm(account)


@app.route('/loan/create', methods=["POST"])
@validate()
def create_loan(body: validators.PydanticLoanRequest):
    loan = models.Loan(**body.__dict__)
    models.db.session.add(loan)
    models.db.session.commit()
    loan = models.Loan.query.get(loan.id)
    transaction = transactions.create_transactions(loan, type=models.TransactionType.charge)
    ledger.add_to_ledger(transaction)
    return models.PydanticLoan.from_orm(loan)

@app.route('/payment/create', methods=["POST"])
def create_payment(body: validators.PydanticPaymentRequest):
    payment = models.Payment(**body.__dict__)
    models.db.session.add(payment)
    models.db.session.commit()
    payment = models.Loan.query.get(payment.id)
    transaction = transactions.create_transactions(payment,  type=models.TransactionType.credit)
    ledger.add_to_ledger(transaction)
    return models.PydanticLoan.from_orm(payment)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)