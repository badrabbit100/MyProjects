from django.db import models


class Game(models.Model):
    room_code = models.CharField(max_length=100)
    game_create = models.CharField(max_length=100)
    ships_creator = models.TextField(max_length=200)
    game_opponent = models.CharField(max_length=100, blank=True, null=True)
    ships_opponent = models.TextField(max_length=200, blank=True, null=True)
    used_cells = models.TextField(max_length=300, blank=True, null=True)
    is_over = models.BooleanField(default=False)

    def __str__(self):
        return f'Creator: {self.game_create}, Opponent: {self.game_opponent}, Status: {self.is_over}'


class Message(models.Model):
    username = models.CharField(max_length=100)
    room_code = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)

    def __str__(self):
        return f'Room: {self.room_code}, Username: {self.username}'
