from requests import get
from urllib.parse import urljoin
from datetime import datetime
from calendar import monthrange


class Worker():

    def __init__(self):
        api_url = 'https://statsapi.web.nhl.com/api/v1/'
        city = 'St. Louis'

        self.main(api_url, city)

    def get_team_ids(self, api_url, city) -> list:
        team_ids = []
        url = urljoin(api_url, 'teams')
        r = get(url).json()
        for line in r['teams']:
            if line['venue']['city'] == city:
                team_ids.append(line['id'])
        return(team_ids)

    def get_game_ids(self, api_url, team_ids, start_day, end_day) -> dict:
        game_id_date = {}
        url = urljoin(api_url, 'schedule')
        for team_id in team_ids:
            payload = {'startDate': start_day, 'endDate': end_day,
                       'teamId': team_id}
            r = get(url, params=payload).json()
            for line in r['dates']:
                for game in line['games']:
                    if game['teams']['home']['team']['id'] == team_id:
                        game_id_date[game['gamePk']] = line['date']
        return(game_id_date)

    def get_game_info(self, api_url, game_ids) -> dict:
        game_info = {}
        for game_id in game_ids:
            url = urljoin(urljoin(api_url, game_id), 'boxscore')
            r = get(url).json()
            

    def get_date_interval(self) -> tuple:
        today = datetime.today()
        if today.month - 1 == 0:
            (year, month) = (today.year - 1, 12)
        else:
            (year, month) = (today.year, today.month - 1)
        start_day = '%s-%s-1' % (year, month)
        end_day = '%s-%s-%s' % (year, month, monthrange(year, month)[1])
        return(start_day, end_day)

    def main(self, api_url, city):
        team_ids = self.get_team_ids(api_url, city)
        start_day, end_day = self.get_date_interval()
        print(self.get_game_ids(api_url, team_ids, start_day, end_day))


if __name__ == '__main__':
    w = Worker()
