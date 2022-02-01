from datetime import datetime

from api_scrap import APIWorker
from common import API_URL, CITY


def get_date_interval() -> tuple:
    today = datetime.today()
    if today.month - 1 == 0:
        (year, month) = (today.year - 1, 12)
    else:
        (year, month) = (today.year, today.month - 1)
    start_date = f'{year}-{month}-1'
    end_date = f'{year}-{month}-31'
    return(start_date, end_date)


if __name__ == '__main__':
    start_date, end_date = get_date_interval()
    w = APIWorker(API_URL, CITY, start_date, end_date)
    w.scrap()
    print(w.game_id_date)
