from django.db import models
from django.utils import timezone

from users.models import Users
from albums.models import generate_comb_guid

class Chatroom(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=36) 
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_comb_guid()
        super(Chatroom, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'chatroom'

class Chatmessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    chatroom = models.ForeignKey('Chatroom', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_id')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chatmessage'

class Chatparticipant(models.Model):
    id = models.BigAutoField(primary_key=True) 
    chatroom = models.ForeignKey('Chatroom', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING, db_column='user_id')

    class Meta:
        managed = True
        db_table = 'chatparticipant'