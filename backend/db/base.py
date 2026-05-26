from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autoflush=False, autocommit=False)
SessionLocal.configure(bind=engine)

Base = declarative_base()
