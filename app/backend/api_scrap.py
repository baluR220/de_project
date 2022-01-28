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
            for n in path['onIce']:
                path_n = path['players']['ID%s' % n]
                if path_n['position']['name'] != 'Goalie':
                    time = path_n['stats']['skaterStats'][
                        'timeOnIce'].split(':')
                    time = int(time[0]) * 60 + int(time[1])
                    all_on_ice[time] = path_n['person']['fullName']
            keys = sorted(all_on_ice.keys(), reverse=True)
            for i in range(3):
                out['%s_top_%s' % (team, i + 1)] = {
                    keys[i]: all_on_ice[keys[i]]
                }
        return out

    def get_date_interval(self) -> tuple:
        today = datetime.today()
        if today.month - 1 == 0:
            (year, month) = (today.year - 1, 12)
        else:
            (year, month) = (today.year, today.month - 1)
        start_day = '%s-%s-1' % (year, month)
        end_day = '%s-%s-31' % (year, month)
        return(start_day, end_day)

    def main(self, api_url, city):
        game_info = {}
        top_on_ice = {}

        team_ids = self.get_team_ids(api_url, city)
        start_day, end_day = self.get_date_interval()
        game_ids = self.get_game_ids(api_url, team_ids, start_day, end_day)

        for game_id in game_ids:
            url = urljoin(api_url, 'game/%s/boxscore' % game_id)
            r = get(url).json()
            game_info[game_id] = self.get_score_names(r)
            top_on_ice[game_id] = self.get_top_on_ice(r)
        print(game_ids, game_info, top_on_ice, sep='\n')


if __name__ == '__main__':
    w = Worker()
