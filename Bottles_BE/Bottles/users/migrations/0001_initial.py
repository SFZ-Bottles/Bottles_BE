# Generated by Django 4.0.7 on 2023-07-18 12:19

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'db_table': 'friendship',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('pw', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.TextField(blank=True, null=True)),
                ('birthdate', models.DateTimeField(blank=True, null=True)),
                ('role', models.CharField(default='default_role', max_length=20)),
                ('status', models.CharField(default='default_role', max_length=20)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
