# Generated by Django 3.2.7 on 2021-09-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='used_cells',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]
