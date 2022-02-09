from requests import get
from urllib.parse import urljoin


class APIWorker():

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

    def get_game_id_date(self, api_url, team_ids, start_date, end_date):
        game_id_date = []
        url = urljoin(api_url, 'schedule')
        for team_id in team_ids:
            payload = {'startDate': start_date, 'endDate': end_date,
                       'teamId': team_id}
            r = get(url, params=payload).json()
            for line in r['dates']:
                for game in line['games']:
                    if game['teams']['home']['team']['id'] == team_id:
                        game_id_date.append({
                            'game_id': game['gamePk'], 'date': line['date']
                        })
        return(game_id_date)

    def get_score_names(self, data) -> dict:
        out = {}
        for team in ['away', 'home']:
            path = data['teams'][team]
            out[f'{team}_name'] = path['team']['name']
            out[f'{team}_score'] = path['teamStats'][
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
                path_n = path['players'][f'ID{n}']
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
                out[f'{team}_top_{i + 1}_time'] = keys[i]
                out[f'{team}_top_{i + 1}_name'] = all_on_ice[keys[i]]
        return out

    def scrap(self):
        game_info = []
        top_on_ice = []
        api_url, city = self.api_url, self.city
        start_date, end_date = self.start_date, self.end_date

        team_ids = self.get_team_ids(api_url, city)
        game_id_date = self.get_game_id_date(api_url, team_ids, start_date,
                                             end_date)

        for game in game_id_date:
            game_id = game['game_id']
            url = urljoin(api_url, f'game/{game_id}/boxscore')
            r = get(url).json()
            d = {'game_id': game_id}
            d.update(self.get_score_names(r))
            game_info.append(d)
            d = {'game_id': game_id}
            d.update(self.get_top_on_ice(r))
            top_on_ice.append(d)

        self.game_date = game_id_date
        self.game_info = game_info
        self.top_time = top_on_ice
