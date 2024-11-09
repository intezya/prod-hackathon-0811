from sqlmodel import SQLModel


class PayDebtRequest(SQLModel):
    trip_id: str
    event_id: str
    debtor_name: str
    pay_value: float

