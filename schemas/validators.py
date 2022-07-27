from typing import Optional
from models.models import PydanticAccount, PydanticTransaction, PydanticLoan, PydanticPayment

class PydanticAccountRequest(PydanticAccount):
    id: Optional[PydanticAccount]
    balance: float
    interest_rate: float

class PydanticLoanRequest(PydanticLoan):
    id: Optional[int]
    purchase_name: str 
    account_id: int 
    amount: float 
    month_remaining: Optional[int]


class PydanticPaymentRequest(PydanticPayment):
    id: Optional[int]
    account_id: int 
    loan_id: int 
    amount: float
