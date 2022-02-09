from datetime import datetime
from os import environ
from time import sleep

from api_scrap import APIWorker
from db_manage import DBWorker
import common as cm


def get_date_interval(for_api=True) -> tuple:
    today = datetime.today()
    if today.month - 1 == 0:
        (year, month) = (today.year - 1, 12)
    else:
        (year, month) = (today.year, today.month - 1)
    if for_api:
        start_date = f'{year}-{month}-1'
        end_date = f'{year}-{month}-31'
    else:
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, 31).date()
    return(start_date, end_date)


def main():
    def update_tables():
        start_date, end_date = get_date_interval()
        api = APIWorker(cm.API_URL, cm.CITY, start_date, end_date)
        api.scrap()
        print('put data in tables')
        db.put_data('game_date', api.game_date)
        db.put_data('game_info', api.game_info)
        db.put_data('top_time', api.top_time)

    db_user = environ['DB_USER']
    db_secret = environ['DB_SECRET']
    db = DBWorker(db_user, db_secret, cm.DB_PREFIX, cm.DB_HOST, cm.DB_NAME)
    db.ensure_tables()
    while True:
        db_date = db.get_db_date()
        if db_date:
            print('tables are not empty')
            start_date, end_date = get_date_interval(for_api=False)
            if start_date <= db_date and db_date <= end_date:
                print('db is actual')
            else:
                print('db is outdated')
                db.delete_data()
                update_tables()
        else:
            print('tables are empty')
            update_tables()
        sleep(cm.SLEEP)


if __name__ == '__main__':
    main()
