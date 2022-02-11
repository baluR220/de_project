from django.shortcuts import render
from nhl_app.models import GameDate, GameInfo, TopTime


def index(request):
    payload = {
        'game_date': GameDate.objects.all(),
        'game_info': GameInfo.objects.all(),
        'top_time': TopTime.objects.all()
    }
    return render(request, 'nhl_app/index.html', payload)
