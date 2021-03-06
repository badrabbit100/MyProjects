# Generated by Django 3.2.7 on 2021-09-08 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_game_used_cells'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_create',
            field=models.CharField(max_length=100, verbose_name='Name of game creator'),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_opponent',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Name of Opponent'),
        ),
        migrations.AlterField(
            model_name='game',
            name='is_over',
            field=models.BooleanField(default=False, verbose_name='Status game'),
        ),
        migrations.AlterField(
            model_name='game',
            name='room_code',
            field=models.CharField(max_length=100, verbose_name='Room Code'),
        ),
        migrations.AlterField(
            model_name='game',
            name='ships_creator',
            field=models.TextField(max_length=200, verbose_name='Ship-cells of creator'),
        ),
        migrations.AlterField(
            model_name='game',
            name='ships_opponent',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Ship-cells of opponent'),
        ),
        migrations.AlterField(
            model_name='game',
            name='used_cells',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='Used cells from game'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=100, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='message',
            name='room_code',
            field=models.CharField(max_length=100, verbose_name='Room Code'),
        ),
        migrations.AlterField(
            model_name='message',
            name='username',
            field=models.CharField(max_length=100, verbose_name='Username'),
        ),
    ]
