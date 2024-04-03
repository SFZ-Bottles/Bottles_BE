import random
from datetime import datetime
from users.models import Users
from albums.models import Albums
from secretmode.models import Usersecretpostmatches

class SecretAlbumConnector:
    @classmethod
    def connect_users_with_album_onlyRandom(self, album_id, user_id, num): #cls, albums_id):
        if num <=0:
            print(f"num is not positive")
            return False
        try:
            # Find the album
            album = Albums.objects.get(id=album_id, is_private=True)
            
            # Find users with is_private=True randomly
            users = Users.objects.filter(is_private=True).exclude(id=user_id).order_by('?')
            target_users = users[:min(num, len(users))]

            # Create Usersecretpostmatches entries
            for user in target_users:
                Usersecretpostmatches.objects.create(
                    user=user,
                    album=album,
                    #is_confirmed=0,
                    connection_date=datetime.now()
                )

            return True
        
        except Albums.DoesNotExist:
            print(f"Album with id {album_id} not found or is not private.")
            return False
        except Exception as e:
            print(f"Error connecting users with secret album: {e}")
            return False

    @classmethod 
    def connect_users_with_album_Demo(self, album_id, user_id):
        temp_num=10
        return self.connect_users_with_album_onlyRandom(album_id=album_id, user_id=user_id, num=temp_num)