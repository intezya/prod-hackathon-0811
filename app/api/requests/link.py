from sqlmodel import SQLModel


class JoinByLinkRequest(SQLModel):
    link: str
    context_type: str
    user_name: str
