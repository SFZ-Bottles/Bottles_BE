from django.db import models
from users.models import Users

class Accountconnection(models.Model):
    nomal_user = models.ForeignKey(Users, models.DO_NOTHING, related_name='normal_user_connections')
    secret_user = models.OneToOneField(Users, models.DO_NOTHING, primary_key=True , related_name='secret_user_connections')
    pw = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'accountconnection'
        unique_together = (('nomal_user', 'secret_user'),)
