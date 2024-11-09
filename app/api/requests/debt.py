from sqlmodel import SQLModel


class PayDebt(SQLModel):
    trip_id: str
    event_id: str
    debtor_name: str
    pay_value: float

