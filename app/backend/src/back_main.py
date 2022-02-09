from datetime import datetime
from os import environ

from api_scrap import APIWorker
from db_manage import DBWorker
import common as cm


def get_date_interval() -> tuple:
    today = datetime.today()
    if today.month - 1 == 0:
        (year, month) = (today.year - 1, 12)
    else:
        (year, month) = (today.year, today.month - 1)
    start_date = f'{year}-{month}-1'
    end_date = f'{year}-{month}-31'
    return(start_date, end_date)


def main():
    db_user = environ['DB_USER']
    db_secret = environ['DB_SECRET']
    db = DBWorker(db_user, db_secret, cm.DB_PREFIX, cm.DB_HOST, cm.DB_NAME)


if __name__ == '__main__':
    start_date, end_date = get_date_interval()
    api = APIWorker(cm.API_URL, cm.CITY, start_date, end_date)
    api.scrap()
    print(api.game_id_date)
