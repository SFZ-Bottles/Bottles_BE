from rest_framework import serializers
from albums.models import Albums, Pages
from users.models import Users
from secretmode.models import Usersecretpostmatches
from local_settings import SERVER_ADDRESS

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = ('id', 'sequence', 'species', 'item')

class AlbumSerializer(serializers.ModelSerializer):
    result = PageSerializer(many=True, source='page')
    
    class Meta:
        model = Albums
        fields = ('id', 'number', 'made_by', 'is_private', 'title', 'preface', 'created_at', 'result')

class AlbumListSerializer(serializers.ModelSerializer):
    #user_id = serializers.CharField(source='user.username')
    user_id = serializers.CharField(source='made_by.username')
    cover_image_url = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    
    class Meta:
        model = Albums
        fields = ('id', 'user_id', 'cover_image_url', 'title', 'created_at')

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner', None)  # 'owner'라는 키로 전달된 값을 인스턴스 변수로 저장
        super(AlbumListSerializer, self).__init__(*args, **kwargs)
        #self.owner = None  # 기본값은 None으로 설정
    
    def get_cover_image_url(self, obj):
        # Find the cover page with species="cover" within the related pages
        cover_page = obj.page.filter(species="cover").first()
        
        if obj.is_private == False :
            if cover_page:
                return SERVER_ADDRESS + "api/image/page/" + cover_page.id + '/'
        
            #커버페이지 없는 경우
            else:
                return SERVER_ADDRESS + "api/image/page/" + '0' + '/'
              

        elif obj.is_private == True:
            user= Users.objects.get(id =self.owner)
            usersecretpostmatch = Usersecretpostmatches.objects.filter(album=obj, user= user ).first()

            #확인 된경우
            if usersecretpostmatch and usersecretpostmatch.is_confirmed:
                if cover_page:
                    return SERVER_ADDRESS + "api/image/page/" + cover_page.id + '/'        
                #커버페이지 없는 경우
                else:
                    return SERVER_ADDRESS + "api/image/page/" + '0' + '/'
            
            #확인 안된경우
            else:
                return SERVER_ADDRESS + "api/image/page/" + '1' + '/'

        
    ################################################################################


class PageResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    order = serializers.IntegerField(source='sequence')
    species = serializers.CharField()
    #data = serializers.CharField(source='item')
    data = serializers.SerializerMethodField()

    class Meta:
        model = Pages
        fields = ('id', 'order', 'species', 'data')
        ordering = ['order']
    
    def get_data(self, obj):
        if obj.species in ['cover', 'image', 'video']:
            return SERVER_ADDRESS + 'api/image/page/' + obj.id +'/'
        
        elif obj.species == 'text':
            return obj.item
        
        return ''  # 다른 species일 경우 빈 문자열 반환
    

class AlbumResponseSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    id = serializers.CharField()
    num = serializers.IntegerField(source='number')
    user_id = serializers.CharField(source='made_by.username')
    is_private = serializers.BooleanField()
    title = serializers.CharField()
    preface = serializers.CharField()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    result = PageResponseSerializer(many=True, source='page')
    
    class Meta:
        model = Albums
        fields = ('message', 'id', 'num', 'user_id', 'is_private', 'title', 'preface', 'created_at', 'result')
        #ordering = ['result__order']

    def get_message(self, obj):
        custom_message = self.context.get('custom_message', 'None') # default : "None"
        return custom_message
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['result'] = sorted(data['result'], key=lambda x: x['order'])  # result 내부의 페이지를 order로 정렬
        return data


