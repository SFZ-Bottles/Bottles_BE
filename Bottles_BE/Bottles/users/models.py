from django.db import models
from django.utils import timezone
import uuid
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=36,default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30)
    pw = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.CharField(unique=True, max_length=40)
    info = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    avatar = models.TextField(blank=True, null=True)
    birthdate = models.DateTimeField(blank=True, null=True)
    role = models.CharField(max_length=20, default='default_role')
    status = models.CharField(max_length=20, default='default_role')
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Friendship(models.Model):
    follower = models.ForeignKey('Users', models.DO_NOTHING, db_column='follower', related_name= 'Friends_follower')
    followed = models.ForeignKey('Users', models.DO_NOTHING, db_column='followed', related_name= 'Friends_followed')
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'friendship'
        unique_together = (('follower', 'followed'),)