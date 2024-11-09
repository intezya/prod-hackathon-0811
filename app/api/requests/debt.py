from sqlmodel import Field, SQLModel


class PayDebtRequest(SQLModel):
    event_id: str
    debtor_name: str
    pay_value: float = Field(gt=0)


class ForgiveDebtRequest(SQLModel):
    event_id: str
    debtor_name: str
