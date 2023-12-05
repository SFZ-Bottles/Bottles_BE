from django.db import models
from users.models import Users
from albums.models import Albums

class Accountconnection(models.Model):
    nomal_user = models.ForeignKey(Users, models.DO_NOTHING, related_name='normal_user_connections')
    secret_user = models.OneToOneField(Users, models.DO_NOTHING, primary_key=True , related_name='secret_user_connections')
    pw = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'accountconnection'
        unique_together = (('nomal_user', 'secret_user'),)

class Usersecretpostmatches(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    album = models.ForeignKey(Albums, models.DO_NOTHING)
    is_confirmed = models.IntegerField()
    connection_date = models.DateTimeField()
    confirmation_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usersecretpostmatches'
