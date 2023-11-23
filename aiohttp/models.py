from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker

PG_USER = 'netology'
PG_PASS = 'netology'
PG_DB = 'aiohttp'
PG_HOST = '192.168.85.4'
PG_PORT = '5431'

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_async_engine(PG_DSN)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class Advert(Base):
    __tablename__ = "api_adverts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    owner = Column(String, nullable=False, unique=True, index=True)
    creation_date = Column(DateTime, server_default=func.now())


