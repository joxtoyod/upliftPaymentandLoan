import enum
import flask_sqlalchemy
from datetime import datetime
from sqlalchemy import Enum
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from typing import Optional

db = flask_sqlalchemy.SQLAlchemy()


class LoanStatus(enum.Enum):
    open = "open"
    pause = "pause"
    close = "close"


class TransactionType(enum.Enum):
    credit = "credit"
    charge = "charge"


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0)
    interest_rate = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_name = db.Column(db.String(50), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    amount = db.Column(db.Float)
    month_remaining = db.Column(db.Integer, default=12)
    status = db.Column(Enum(LoanStatus))
    created_at = db.Column(db.DateTime, default=datetime.now)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    loan_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    amount = db.Column(db.Float)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey("loan.id"))
    type = db.Column(Enum(TransactionType))
    amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey("transaction.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)


PydanticAccount = sqlalchemy_to_pydantic(Account)
PydanticTransaction = sqlalchemy_to_pydantic(Transaction)
PydanticLoan = sqlalchemy_to_pydantic(Loan)
PydanticPayment = sqlalchemy_to_pydantic(Payment)
