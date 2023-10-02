from django.contrib import admin
from .models import Albums, Pages
from users.models import Users, Friendship
from comments.models import Comments, Reply

class AlbumsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'made_by_username', 'is_private', 'created_at', 'updated_at')

    def made_by_username(self, obj):
        return obj.made_by.username
    made_by_username.short_description = 'Made By'

class PagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'album_id', 'species', 'sequence', 'item')

    def album_id(self, obj):
        return obj.album.id
    album_id.short_description = 'Album ID'

class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'create_at')

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('follower_username', 'followed_username', 'created_at')
    ordering = ('follower__username',)  # follower_username 메서드와 연관된 필드를 기준으로 정렬

    def follower_username(self, obj):
        return obj.follower.username

    def followed_username(self, obj):
        return obj.followed.username

    '''    
    # 더미 필드 추가
    def id(self, obj):
        return obj.pk
    
    follower_username.short_description = 'Follower'
    followed_username.short_description = 'Followed'
    id.short_description = 'ID'
    '''

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'made_by_username', 'album', 'content', 'created_at')

    def made_by_username(self, obj):
        return obj.made_by.username
    made_by_username.short_description = 'Made By'

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('parent_comment', 'child_comment')

admin.site.register(Albums, AlbumsAdmin)
admin.site.register(Pages, PagesAdmin)
admin.site.register(Users, UsersAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Reply, ReplyAdmin)

#python manage.py createsuperuser
