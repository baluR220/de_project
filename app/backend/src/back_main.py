from datetime import datetime
from calendar import monthrange

import api_scrap
from common import API_URL, CITY


def get_date_interval() -> tuple:
    today = datetime.today()
    if today.month - 1 == 0:
        (year, month) = (today.year - 1, 12)
    else:
        (year, month) = (today.year, today.month - 1)
    start_date = '%s-%s-1' % (year, month)
    end_date = '%s-%s-31' % (year, month)
    return(start_date, end_date)


if __name__ == '__main__':
    start_date, end_date = get_date_interval()
    w = api_scrap.Worker(API_URL, CITY, start_date, end_date)
    w.scrap()
    print(w.game_id_date)
