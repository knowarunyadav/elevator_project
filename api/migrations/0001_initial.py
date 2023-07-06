# Generated by Django 2.2.7 on 2023-07-02 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('up', 'up'), ('down', 'down'), ('ideal', 'ideal')], default='ideal', max_length=64)),
                ('door', models.CharField(choices=[('open', 'open'), ('close', 'close')], default='close', max_length=64)),
                ('running_status', models.CharField(choices=[('start', 'start'), ('stop', 'stop')], default='stop', max_length=64)),
                ('current_status', models.CharField(choices=[('open', 'open'), ('close', 'close')], default='close', max_length=64)),
                ('available_status', models.CharField(choices=[('available', 'available'), ('busy', 'busy')], default='available', max_length=64)),
                ('operational', models.BooleanField(default=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_floor', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_count', models.IntegerField(default=0)),
                ('request_floor', models.IntegerField(default=0)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Elevator')),
            ],
        ),
    ]