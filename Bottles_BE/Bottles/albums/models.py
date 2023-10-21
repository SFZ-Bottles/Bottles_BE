from django.db import models
from django.utils import timezone
from users.models import Users

import uuid
from django.db import models
from django.utils import timezone

from datetime import datetime

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

def generate_comb_guid():
    now = datetime.now()
    timestamp = int(now.timestamp())
    uuid_part = uuid.uuid4().int & (1 << 64) - 1
    comb_guid = "{:014x}{:016x}".format(timestamp, uuid_part)
    return comb_guid


class Albums(models.Model):
    id = models.CharField(primary_key=True, max_length=36,editable=False)
    made_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='made_by')
    is_private = models.IntegerField()
    title = models.TextField(null=True)
    preface = models.TextField(null=True)
    number = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
            if not self.id:
                self.id = generate_comb_guid()
            super(Albums, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'albums'


class Pages(models.Model):
    id = models.CharField(primary_key=True, max_length=36,editable=False)
    album = models.ForeignKey(Albums, models.DO_NOTHING,related_name='page')
    species = models.CharField(max_length=10)
    sequence = models.CharField(max_length=10)
    item = models.TextField()


    def save(self, *args, **kwargs):
            if not self.id:
                 self.id = generate_comb_guid()
            super(Pages, self).save(*args, **kwargs)


    class Meta:
        managed = False
        db_table = 'pages'
