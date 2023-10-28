from fastapi_jwt_auth import AuthJWT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.utils.utils import getConnectionParameters

params = getConnectionParameters("local")
authjwt = AuthJWT()
DATABASE_URL = f"mysql://{params['user']}:@{params['host']}/{params['db']}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
sql = SessionLocal()



