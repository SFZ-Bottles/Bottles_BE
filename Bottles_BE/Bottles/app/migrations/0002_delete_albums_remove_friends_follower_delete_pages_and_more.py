# Generated by Django 4.0.7 on 2023-07-18 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Albums',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='follower',
        ),
        migrations.DeleteModel(
            name='Pages',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='reply',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Friends',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
