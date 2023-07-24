import jwt
from users.models import Users
from local_settings import JWT_SECRET_KEY

def Authenticate(request):
    token = request.COOKIES.get('token')
    if not token :
        print("없음")
        return False
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("변조됨")
        return False
    
    user = Users.objects.get(username = payload['id'])
    return(user.id)