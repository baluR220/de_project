from django.urls import include, path


urlpatterns = [
    path('', include('nhl_app.urls'))
]
