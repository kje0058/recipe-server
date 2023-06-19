# 개발하면서 유용한 함수들 모아두고 사용

from passlib.hash import pbkdf2_sha256 # 단방향 암호화 라이브러리
from config import Config

# 1. 원문 비밀번호를 단방향으로 암호화 하는 함수
def hash_password( original_password ) : # 원래 입력한 비밀번호
    password = pbkdf2_sha256.hash( original_password + Config.SALT) # 암호화 식
    return password

# 2. 유저가 입력한  비밀번호가 맞는지 체크하는 함수
def check_password( original_password, hashed_password ) : 
    check = pbkdf2_sha256.verify(original_password + Config.SALT, hashed_password) # verify : 맞는지 확인해주는 검증 함수
    return check # 같으면 True, 다르면 False (함수 안에 내장)