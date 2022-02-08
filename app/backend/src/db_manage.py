import sqlalchemy as sa


class DBWorker():

    def __init__(self, user, secret, db_prefix, db_host, db_name):
        engine_literal = f'{db_prefix}{user}:{secret}@{db_host}/{db_name}'
        self.engine = sa.create_engine(engine_literal, future=True)

    def set_tables(self):
        meta_obj = sa.MetaData()
        meta_obj.bind = self.engine
        sa.Table(
            'game_date', meta_obj,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('game_id', sa.Integer),
            sa.Column('date', sa.Date)
        )
        sa.Table(
            'game_info', meta_obj,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('game_id', sa.Integer,),
            sa.Column('away_name', sa.String(50)),
            sa.Column('away_score', sa.Integer),
            sa.Column('home_name', sa.String(50)),
            sa.Column('home_score', sa.Integer),
        )
        sa.Table(
            'top_score', meta_obj,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('game_id', sa.Integer),
            sa.Column('away_top_1_name', sa.String(50)),
            sa.Column('away_top_1_time', sa.Integer),
            sa.Column('away_top_2_name', sa.String(50)),
            sa.Column('away_top_2_time', sa.Integer),
            sa.Column('away_top_3_name', sa.String(50)),
            sa.Column('away_top_3_time', sa.Integer),
            sa.Column('home_top_1_name', sa.String(50)),
            sa.Column('home_top_1_time', sa.Integer),
            sa.Column('home_top_2_name', sa.String(50)),
            sa.Column('home_top_2_time', sa.Integer),
            sa.Column('home_top_3_name', sa.String(50)),
            sa.Column('home_top_3_time', sa.Integer),
        )

        return meta_obj

    def get_tables(self):
        meta_obj = sa.MetaData()

        @sa.event.listens_for(meta_obj, "column_reflect")
        def genericize_datatypes(inspector, tablename, column_dict):
            column_dict["type"] = column_dict["type"].as_generic()

        meta_obj.bind = self.engine
        meta_obj.reflect(self.engine)
        return meta_obj

    def ensure_tables(self):
        meta_old = self.get_tables()
        meta_new = self.set_tables()
        t_old = meta_old.tables
        t_new = meta_new.tables
        if t_old:
            if len(t_old.keys()) != len(t_new.keys()):
                drop_old = True
            else:
                for t_name in t_new.keys():
                    if t_name not in t_old.keys():
                        drop_old = True
                        break
                    if not t_new[t_name].compare(t_old[t_name]):
                        drop_old = True
                        break
                    drop_old = False
            if drop_old:
                print('drop old tables')
                meta_old.drop_all()
        else:
            drop_old = True
        if drop_old:
            print('create new tables')
            meta_new.create_all()
        self.meta_obj = meta_new

    def put_data(self, table_name, data):
        with self.engine.connect() as connect:
            connect.execute(sa.insert(self.meta_obj.tables[table_name]), data)
            connect.commit()

    def delete_data(self):
        for table in reversed(self.meta_obj.sorted_tables):
            with self.engine.connect() as connection:
                connection.execute(table.delete())
