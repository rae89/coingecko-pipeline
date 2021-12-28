import os
import sqlalchemy as db


USER = "root"
PASSWORD = os.environ["MYSQL_PASSWORD"]
PORT = os.environ["MYSQL_PORT"]
DATABASE = os.environ["MYSQL_DATABASE"]
HOST = os.environ["MYSQL_HOST"]


engine = db.create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"
)