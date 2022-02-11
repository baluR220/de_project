from django.db import models


class GameDate(models.Model):
    game_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_date'
        app_label = 'nhl_app'


class GameInfo(models.Model):
    game_id = models.IntegerField(blank=True, null=True)
    away_name = models.CharField(max_length=50, blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    home_name = models.CharField(max_length=50, blank=True, null=True)
    home_score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_info'
        app_label = 'nhl_app'


class TopTime(models.Model):
    game_id = models.IntegerField(blank=True, null=True)
    away_top_1_name = models.CharField(max_length=50, blank=True, null=True)
    away_top_1_time = models.IntegerField(blank=True, null=True)
    away_top_2_name = models.CharField(max_length=50, blank=True, null=True)
    away_top_2_time = models.IntegerField(blank=True, null=True)
    away_top_3_name = models.CharField(max_length=50, blank=True, null=True)
    away_top_3_time = models.IntegerField(blank=True, null=True)
    home_top_1_name = models.CharField(max_length=50, blank=True, null=True)
    home_top_1_time = models.IntegerField(blank=True, null=True)
    home_top_2_name = models.CharField(max_length=50, blank=True, null=True)
    home_top_2_time = models.IntegerField(blank=True, null=True)
    home_top_3_name = models.CharField(max_length=50, blank=True, null=True)
    home_top_3_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'top_time'
        app_label = 'nhl_app'
