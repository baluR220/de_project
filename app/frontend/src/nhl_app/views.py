from django.shortcuts import render
from nhl_app.models import GameDate, GameInfo, TopTime


def index(request):

    def time(seconds):
        m = int(seconds) // 60
        s = int(seconds) - m * 60
        return(f'{m}:{s:02d}')

    games = []
    game_date = GameDate.objects.all()
    game_info = GameInfo.objects.all()
    top_time = TopTime.objects.all()
    for item in game_date:
        info = game_info.get(game_id=item.game_id)
        top = top_time.get(game_id=item.game_id)
        game = {
            'date': item.date,
            'away_name': info.away_name,
            'away_score': info.away_score,
            'home_name': info.home_name,
            'home_score': info.home_score,
            'away_top_1_name': top.away_top_1_name,
            'away_top_1_time': time(top.away_top_1_time),
            'away_top_2_name': top.away_top_2_name,
            'away_top_2_time': time(top.away_top_2_time),
            'away_top_3_name': top.away_top_3_name,
            'away_top_3_time': time(top.away_top_3_time),
            'home_top_1_name': top.home_top_1_name,
            'home_top_1_time': time(top.home_top_1_time),
            'home_top_2_name': top.home_top_2_name,
            'home_top_2_time': time(top.home_top_2_time),
            'home_top_3_name': top.home_top_3_name,
            'home_top_3_time': time(top.home_top_3_time),

        }
        games.append(game)
    return render(request, 'nhl_app/index.html', {'games': games})
