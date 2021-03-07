from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.sqlite', echo=True)

Base = declarative_base()


class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    id_coingecko = Column(Integer)
    symbol = Column(String)
    name = Column(String)

    def __repr__(self):
       return f"<Coin(name='{self.id_coingecko}', fullname='{self.symbol}', nickname='{self.name}')>"


Session = sessionmaker(bind=engine)
session = Session()