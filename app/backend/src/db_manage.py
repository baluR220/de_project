from os import environ

import sqlalchemy as sa

from common import DB_HOST, DB_PREFIX, DB_NAME


class DBWorker():

    def __init__(self, user, secret, db_prefix, db_host, db_name):
        engine_literal = f'{db_prefix}{user}:{secret}@{db_host}/{db_name}'
        self.engine = sa.create_engine(engine_literal, echo=True, future=True)


if __name__ == '__main__':
    user = environ['DB_USER']
    secret = environ['DB_SECRET']
    w = DBWorker(user, secret, DB_PREFIX, DB_HOST, DB_NAME)
