from django.db import models
from users.models import Users
from albums.models import Albums, generate_comb_guid
from django.utils import timezone

class Comments(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    album = models.ForeignKey(Albums, models.DO_NOTHING)
    made_by = models.ForeignKey(Users, models.DO_NOTHING, db_column='made_by', related_name= 'comments_made_by')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    mentioned_user = models.ForeignKey(Users, models.DO_NOTHING, null=True,  related_name= 'comments_mentioned_user_id')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_comb_guid()
        super(Comments, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'comments'

class Reply(models.Model):
    parent_comment = models.ForeignKey(Comments, models.DO_NOTHING, related_name= 'reply_parent')
    child_comment = models.OneToOneField(Comments, models.DO_NOTHING, related_name= 'reply_child', primary_key=True)

    class Meta:
        managed = False
        db_table = 'reply'
        unique_together = (('parent_comment', 'child_comment'),)

    def __iter__(self):
        # child_comment를 iterable하게 반환합니다.
        return iter([self.child_comment])