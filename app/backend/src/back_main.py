import http.server
from datetime import datetime
from os import environ
from time import sleep
from threading import Thread

from api_scrap import APIWorker
from db_manage import DBWorker
import common as cm


class BackWorker():
    def __init__(self):
        self.db_user = environ['DB_USER']
        self.db_secret = environ['DB_SECRET']
        self.db = DBWorker(self.db_user, self.db_secret, cm.DB_PREFIX,
                           cm.DB_HOST, cm.DB_NAME)

    def get_date_interval(self, for_api=True) -> tuple:
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

    def update_tables(self, db):
        start_date, end_date = self.get_date_interval()
        api = APIWorker(cm.API_URL, cm.CITY, start_date, end_date)
        api.scrap()
        print('put data in tables')
        db.put_data('game_date', api.game_date)
        db.put_data('game_info', api.game_info)
        db.put_data('top_time', api.top_time)

    def keep_db_updated(self):
        db_date = self.db.get_db_date()
        if db_date:
            print('tables are not empty')
            start_date, end_date = self.get_date_interval(for_api=False)
            if start_date <= db_date and db_date <= end_date:
                print('db is actual')
            else:
                print('db is outdated')
                self.db.delete_data()
                self.update_tables(self.db)
        else:
            print('tables are empty')
            self.update_tables(self.db)

    def work(self):
        self.db.ensure_tables()
        while True:
            self.keep_db_updated()
            sleep(cm.SLEEP)


if __name__ == '__main__':

    back = BackWorker()

    class CustomHandler(http.server.BaseHTTPRequestHandler):

        def set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self.set_headers()
            back.keep_db_updated()

        def do_HEAD(self):
            self.set_headers()

    def start_server(server_class=http.server.HTTPServer,
                     handler_class=CustomHandler):
        server_address = ('', 8080)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

    Thread(target=start_server, daemon=True).start()
    back.work()
