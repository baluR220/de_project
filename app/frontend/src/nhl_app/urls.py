from django.urls import path

from . import views


app_name = 'nhl_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('update_db/', views.update_db),
    path('result/', views.result),
]
