import jwt
from jwt.exceptions import InvalidSignatureError
from users.models import Users
from local_settings import JWT_SECRET_KEY

def Authenticate(request):

    
    
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token :
        token = request.COOKIES.get('token')
        if not token :
            return False
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        user = Users.objects.get(username = payload['id'])
        return(user.id)
    
    except jwt.ExpiredSignatureError:
        print("토큰 만료")
        return False
    
    except InvalidSignatureError:
        print("올바르지 않은 시그니처")
        return False
    
    except Users.DoesNotExist:
        print("사용자 없음")
        return False
    
    except Exception as e:
        print("기타 에러:", e)
        return False
    
   