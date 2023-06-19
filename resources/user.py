from flask_restful import Resource # 리소스 라이브러리 데이터 동작 코드
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection
from email_validator import validate_email, EmailNotValidError
from utils import check_password, hash_password
from flask_jwt_extended import create_access_token
import datetime

class UserRegisterResource(Resource) : # 플라스크 라이브러리의 리소스에서 post get 등이 담긴 함수를 받아 씀
# 함수가 들어있는 플라스크 생성!
    def post(self) : 

        # 포스트맨에서 데이터 확인!
        # {
        #     "username":"홍길동",
        #     "email":"abc@naver.com",
        #     "password":"1234"
        # }

        # 1. 클라이언트가 보낸 데이터를 확인한다.
        data = request.get_json() # body의 json의 데이터를 받아옴
        print(data) 

        # 2. 이메일 주소형식이 올바른지 확인한다.
        # $pip install email-validator 설치
        # import email-validator 라이브러리
        try : 
            validate_email( data['email'] )
        except EmailNotValidError as e : 
            print(e)
            return {'result':'fail', 'error':str(e)}, 400
        
        # 3. 비밀번호 길이가 유효한지 체크한다.
        #    만약 비번이 4자리이상, 12자리 이하라고 한다면,
        if len(data['password']) < 4 or len(data['password']) > 12 : # 비정상 부터 체크 
            return {'result':'fail', 'error':'비번 길이 에러'}, 400
        
        # 4. 비밀번호를 암호화한다.
        # $pip install passlib 설치
        # $pip install psycopg2-binary 설치
        # hash : 단방향 암호화로 해시 함수를 이용하여 유니크하게 암호화된 문자열로 바꿔줌, 복구안댐
        hashed_password = hash_password(data['password']) # 데이터의 password를 암호화하라!
        print(str(hashed_password))

        # 5. DB에 이미 회원정보가 있는지 확인한다.

        try :
            connection = get_connection()
            query = '''select *
                    from user
                    where email=%s;'''
            record = ( data['email'], )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()
            print(result_list)

            if len(result_list) == 1 : # 이메일이 1이면 이미 가입한 사람이다
                return {'result':'fail', 'error' : '이미 회원가입 한 사람'}, 400

            # 회원이 아니므로, 회원가입 코드를 작성한다.
            # DB에 저장
            # connection은 이미 있으니 제외하고 작성
            query = '''insert into user
                    (username, email, password)
                    values
                    (%s, %s, %s);'''
            record = ( data['username'],
                      data['email'],
                      hashed_password ) # 단방향 암호화된 패스워드 불러와야함
            cursor = connection.cursor()
            cursor.execute(query, record) # 쿼리랑 레코드를 실행하라

            connection.commit() # 데이터 베이스에 넣어라

            ## DB에 데이터를 insert 한 후에 그 insert 된 행의 아이디를 가져오는 코드
            ## 회원가입시, user_id가 노출되지 않게 인증토큰이 필요해, 클라이언트에게 보내줘야함.
            user_id = cursor.lastrowid

            cursor.close()
            connection.close()


        except Error as e :
            print(e)
            return { 'result' : 'fail', 'error':str(e) }, 500
        
        access_token = create_access_token( user_id )
        # create_access_token(user_id, expires_delta=datetime.timedelta(days=10))
        # 10일동안 데이터 유지하겠다.

        return { 'result' : 'success', 'access_token' : access_token }, 200


# 로그인 관련 개발

class UserLoginResource(Resource) : 
    def post(self) :
        # 1. 클라이언트로부터 데이터를 받아온다.
        data = request.get_json()
        print(data)

        # 2. 이메일 주소로 DB에 select한다.
        try : 
            connection = get_connection()
            query = '''select *
                    from user
                    where email=%s;'''
            record = (data['email'], )

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()
            
            cursor.close()
            connection.close()
        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)},500
        
        if len(result_list) == 0 : # 이메일이 없으면
            return {'result':'fail', 'error':'회원가입한 사람이 아님'}, 400

        # 3. 비밀번호가 일치하는지 확인한다.
        #    암호화된 비밀번호가 일치하는지 확인해야함.
        print(result_list)
        check = check_password( data['password'], result_list[0]['password'] )

        # 비밀번호 일치하는지 확인할 때, 사용하면 안되는 쿼리문!!!
        # select *
        # from user
        # where email = 'abcd@naver.com' and password = 'fgcgef';
        # -- 암호화할때마다 똑같은 것이 나오지 않음.
        # -- 암호화시 모두 다르게되므로 이 select 문으로는 암호화된 패스워드를 체크할 수 없다.

        if check == False :
            return {'result':'fail', 'error':'비밀번호가 틀림'}, 400

        # 4. 클라이언트에게 user_id 데이터를 보내준다._보안토큰 변경한 것으로

        access_token = create_access_token(result_list[0]['id'])

        return { 'result' : 'success', 'access_token' : access_token }, 200
    
        # 클라이언트는 user_id를 가지고 있어야 한다.
        # 로그인을 하면 내 정보를 가져와야함
        # 자동로그인에도 user_id가 필요하다.
        # user_id도 노출되면 안되므로 암호화 해야함. -> 인증토큰 처리해야함