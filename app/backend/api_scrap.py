from requests import get
from urllib.parse import urljoin

from common import API_URL, CITY


class Worker():

    def __init__(self, api_url, city, start_date, end_date):
        self.api_url = api_url
        self.city = city
        self.start_date = start_date
        self.end_date = end_date

    def get_team_ids(self, api_url, city) -> list:
        team_ids = []
        url = urljoin(api_url, 'teams')
        r = get(url).json()
        for line in r['teams']:
            if line['venue']['city'] == city:
                team_ids.append(line['id'])
        return(team_ids)

    def get_game_id_date(self, api_url, team_ids, start_date, end_date) -> dict:
        game_id_date = {}
        url = urljoin(api_url, 'schedule')
        for team_id in team_ids:
            payload = {'startDate': start_date, 'endDate': end_date,
                       'teamId': team_id}
            r = get(url, params=payload).json()
            for line in r['dates']:
                for game in line['games']:
                    if game['teams']['home']['team']['id'] == team_id:
                        game_id_date[game['gamePk']] = line['date']
        return(game_id_date)

    def get_score_names(self, data) -> dict:
        out = {}
        for team in ['away', 'home']:
            path = data['teams'][team]
            out['%s_name' % team] = path['team']['name']
            out['%s_score' % team] = path['teamStats'][
                'teamSkaterStats']['goals']
        return out

    def get_top_on_ice(self, data) -> dict:
        out = {}
        for team in ['away', 'home']:
            path = data['teams'][team]
            all_on_ice = {}
            if path['onIce']:
                path_id = path['onIce']
            else:
                path_id = path['skaters']
            for n in path_id:
                path_n = path['players']['ID%s' % n]
                if path_n['position']['name'] != 'Goalie':
                    try:
                        time = path_n['stats']['skaterStats'][
                            'timeOnIce'].split(':')
                    except KeyError:
                        time = '0:0'.split(':')
                    time = int(time[0]) * 60 + int(time[1])
                    all_on_ice[time] = path_n['person']['fullName']
            keys = sorted(all_on_ice.keys(), reverse=True)
            for i in range(3):
                out['%s_top_%s' % (team, i + 1)] = {
                    keys[i]: all_on_ice[keys[i]]
                }
        return out

    def scrap(self):
        game_info = {}
        top_on_ice = {}
        api_url, city = self.api_url, self.city
        start_date, end_date = self.start_date, self.end_date

        team_ids = self.get_team_ids(api_url, city)
        game_id_date = self.get_game_id_date(api_url, team_ids, start_date,
                                             end_date)

        for game_id in game_id_date.keys():
            url = urljoin(api_url, 'game/%s/boxscore' % game_id)
            r = get(url).json()
            game_info[game_id] = self.get_score_names(r)
            top_on_ice[game_id] = self.get_top_on_ice(r)

        self.game_id_date = game_id_date
        self.game_info = game_info
        self.top_on_ice = top_on_ice


if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2022-01-31'
    w = Worker(API_URL, CITY, start_date, end_date)
    w.scrap()
    print(w.game_id_date)
