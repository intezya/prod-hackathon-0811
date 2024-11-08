from app.internal.config import settings
from sqlmodel import Session, create_engine

engine = create_engine(str(settings.POSTGRES_DATABASE_URI))

def get_db():
    with Session(engine) as session:
        yield session
