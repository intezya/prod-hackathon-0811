from sqlmodel import SQLModel


class JoinByLinkRequest(SQLModel):
    link: str
