from sqlmodel import SQLModel


class ConnectMainWebsocketRequest(SQLModel):
    user_name: str
    id_from_link: str
