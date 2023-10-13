from fastapi import Depends
from app.configuration.config import SessionLocal


def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()