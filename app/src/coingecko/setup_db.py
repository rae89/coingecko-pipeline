import sqlalchemy as db
from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import CreateSchema
from mysql_engine import engine
from sqlalchemy import event, DDL, select

Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Asset(Base):
    __tablename__ = "asset"
    __table_args__ = {"schema": "coingecko", "mysql_charset": "utf8mb4"}
    inserted_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    id = Column(String(200), primary_key=True)
    symbol = Column(String(200))
    name = Column(String(200))
    prices_usd = relationship("PriceUSD")


class PriceUSD(Base):
    __tablename__ = "price_usd"
    __table_args__ = {"schema": "coingecko", "mysql_charset": "utf8mb4"}
    inserted_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP"),
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    id = Column(Integer, primary_key=True)
    asset_id = Column(String(200), ForeignKey("coingecko.asset.id"))
    price = Column(Float)
    market_cap = Column(Float)
    volume_24hrs = Column(Float)


if __name__ == "__main__":
    event.listen(
        Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS coingecko")
    )
    Base.metadata.create_all(engine)
    print("COINGECKO PRICES DATABASE SETUP SUCCESSFULL!!!!")