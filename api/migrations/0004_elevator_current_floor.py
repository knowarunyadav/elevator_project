# Generated by Django 2.2.7 on 2023-07-04 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20230704_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='elevator',
            name='current_floor',
            field=models.IntegerField(default=0),
        ),
    ]