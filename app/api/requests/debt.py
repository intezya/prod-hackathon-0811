from sqlmodel import SQLModel


class PayDebtRequest(SQLModel):
    event_id: str
    debtor_name: str
    pay_value: float


class ForgiveDebtRequest(SQLModel):
    event_id: str
    debtor_name: str
