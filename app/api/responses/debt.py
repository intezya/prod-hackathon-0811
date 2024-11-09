from sqlmodel import SQLModel


class PayDebtResponse(SQLModel):
    new_value: float
