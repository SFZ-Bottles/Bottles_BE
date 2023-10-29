import random
import string


# 랜덤한 문자열 생성
class RandomString:
    
    def __init__(self) -> None:
        pass

    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string