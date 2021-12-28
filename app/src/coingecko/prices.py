import sqlalchemy as db
from sqlalchemy.sql import table, column, select, update
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from pycoingecko import CoinGeckoAPI
from itertools import chain
from setup_db import PriceUSD
import time
from mysql_engine import engine


def get_asset_ids():
    asset = db.Table(
        "asset", metadata, schema="coingecko", autoload=True, autoload_with=engine
    )
    select_stmt = select([asset.columns.id]).distinct()
    output = session.execute(select_stmt).fetchall()
    asset_ids = list(chain(*output))
    return asset_ids


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def handle_prices_usd(prices):
    result = []
    for asset_id, data in prices.items():
        print("ASSET_ID: ", asset_id)
        print("DATA: ", data)
        if data:
            result.append(
                PriceUSD(
                    asset_id=asset_id,
                    price=data["usd"],
                    market_cap=data["usd_market_cap"],
                    volume_24hrs=data["usd_24h_vol"],
                )
            )
    return result


def get_prices(ids=None, currency="usd"):
    cg = CoinGeckoAPI()
    prices = cg.get_price(
        ids=chunk,
        vs_currencies=[currency],
        include_market_cap=True,
        include_24hr_vol=True,
    )
    return prices


if __name__ == "__main__":
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    metadata = db.MetaData()

    with session.begin():
        asset_ids = get_asset_ids()

    with session.begin():
        for chunk in list(chunks(asset_ids, 500)):
            prices = get_prices(ids=chunk, currency="usd")
            time.sleep(0.2)
            price_objects = handle_prices_usd(prices)
            session.bulk_save_objects(price_objects)