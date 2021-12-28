import sqlalchemy as db
from sqlalchemy.sql import table, column, select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from pycoingecko import CoinGeckoAPI
from mysql_engine import engine


def get_coins():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_list()
    return coins


def upsert_coins(metadata):
    table = db.Table(
        "asset", metadata, schema="coingecko", autoload=True, autoload_with=engine
    )
    insert_stmt = insert(table).values(coins)
    upsert_stmt = insert_stmt.on_duplicate_key_update(
        id=insert_stmt.inserted.id,
        symbol=insert_stmt.inserted.symbol,
        name=insert_stmt.inserted.name,
    )
    return upsert_stmt


if __name__ == "__main__":
    coins = get_coins()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    metadata = db.MetaData()
    with session.begin():
        upsert_query = upsert_coins(metadata)
        session.execute(upsert_query)