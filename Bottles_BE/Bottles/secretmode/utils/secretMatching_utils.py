import random
import string


# 랜덤한 문자열 생성
class secretMatching:
    
    def __init__(self, user_id,  ):
        pass

    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string
    
'''
1. 비밀 앨범 생성시 유저랑 매칭
2. 비밀게시글 구준히 업데이트 해야하나...?
3. ....
'''