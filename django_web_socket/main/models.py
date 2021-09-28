from django.db import models


class Game(models.Model):
    """ This is the game model keep data about players, ships and status"""
    room_code = models.CharField(max_length=100, verbose_name='Room Code')
    game_create = models.CharField(max_length=100, verbose_name='Name of game creator')
    ships_creator = models.TextField(max_length=200, verbose_name='Ship-cells of creator')
    game_opponent = models.CharField(max_length=100, blank=True, null=True, verbose_name='Name of Opponent')
    ships_opponent = models.TextField(max_length=200, blank=True, null=True, verbose_name='Ship-cells of opponent')
    used_cells = models.TextField(max_length=300, blank=True, null=True, verbose_name='Used cells from game')
    is_over = models.BooleanField(default=False, verbose_name='Status game')

    def __str__(self):
        return f'Creator: {self.game_create}, Opponent: {self.game_opponent}, Status: {self.is_over}'


class Message(models.Model):
    """ This model keep all data about messages from socket"""
    username = models.CharField(max_length=100, verbose_name='Username')
    room_code = models.CharField(max_length=100, verbose_name='Room Code')
    message = models.CharField(max_length=100, verbose_name='Message')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)

    def __str__(self):
        return f'Room: {self.room_code}, Username: {self.username}'
