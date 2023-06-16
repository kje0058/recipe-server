from flask_restful import Resource # 리소스 라이브러리 데이터 동작 코드
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection

# api 동작하는 코드를 만들기 위해서는 class(클래스)를 만들어야 한다.

# class란? 비슷한 데이터끼리 모아놓은 것(테이블과 비슷)
# class는 변수와 함수로 구성된 묶음
# 테이블과 다른점 : 함수가 있다는 점!

# API를 만들기 위해서는,
# flask_restful 라이브러리의 Resource 클래스를!!!
# 상속해서 만들어야 한다. 파이썬에서 상속은 괄호!
# class 클래스이름(Resource) -- import 한 것

class RecipeListResource(Resource) :

    def post(self) :

        # 포스트로 요청한 것을 처리하는 코드 작성은 우리가!
        
        # 로직(순서) 이해

        # 1. 클라이언트가 보낸 데이터를 받아온다.
        data = request.get_json()
        print(data)
        # 데이터 확인용으로 포스트맨에서 가져옴
        # {
        #     "name" : "김치찌개",
        #     "description" : "맛있게 끓이는 방법",
        #     "num_of_servings" : 4,
        #     "cook_time" : 30,
        #     "directions" : "고기볶고 김치넣고 물붓고 두부넣고",
        #     "is_pulbish" : 1
        # }

        # 2. 받아온 데이터 DB에 저장한다.

        
        try :  # 에러났을때
            # 2-1. 데이터베이스를 연결한다.(connection)
            connection = get_connection()

            # 2-2. 쿼리문을 만든다._ 컬럼은 mysql workbench에서 만들어서 가져옴(레시피DB)
            #### 중요!! 컬럼과 매칭되는 데이터만 %s(포맷팅)로 바꿔준다._유저입력을 위해
            query = '''insert into recipe
                    (name, description, num_of_servings, cook_time,
                        directions , is_publish)
                    values
                    (%s, %s, %s, %s, %s, %s);'''

            
            # 2-3. 쿼리에 매칭되는 변수 처리! 중요!! 튜플로 처리!!
            record = ( data['name'], data['description'],
                      data['num_of_servings'],
                       data['cook_time'],
                        data['directions'],
                         data['is_publish'] )
            
            # 2-4. 커서를 가져온다.
            cursor = connection.cursor()

            # 2-5. 쿼리문을 커서로 실행한다.
            cursor.execute(query, record)

            # 2-6. DB에 반영 완료하라는, commit 해줘야 한다.
            connection.commit()

            # 2-7. 자원 해제_커서 클로즈, 커넥션 클로즈
            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            return {'result' : 'fail', 'error' : str(e) }, 500

        # 3. 에러가 났으면 에러났다고 알려주고(return)
        #    그렇지 않으면 잘 저장되었다고 알려준다.



        return {'result' : 'success'}
    
    def get(self) :
        # 코드 작성.
        print("레시피 가져오는 API 동작했음.")

        # 로직(순서)

        # 1. 클라이언트로부터 데이터를 받아온다.       
           
        try :
            
            # 2. 저장된 레시피 리스트를 DB로부터 가져온다.

            # 2-1. DB 커넥션
            connection = get_connection()

            # 2-2. 쿼리문 만든다.
            query = '''select * from recipe
                    order by createdAt desc;'''
            
            # 2-3. 변수 처리할 부분은 변수처리한다.
            # 없음

            # 2-4. 커서 가져온다
            cursor = connection.cursor(dictionary=True) # 딕셔너리 형태로 가지고온다.

            # 2-5. 쿼리문을 커서로 실행한다.
            cursor.execute(query)

            # 2-6. 실행 결과를 가져온다.
            result_list = cursor.fetchall() # 전부다 가지고와라
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e : 
            print(e)
            return {'result' : 'fail', 'error':str(e)}, 500
            # , 상태코드 : 내가 보낸 http 상태코드를 클라이언트한테 보냄
        
        # 3. 데이터 가공이 필요하면, 가공한 후에 클라이언트에 응답한다.

        i = 0
        for row in result_list : # result_list에서 행을 하나씩 가져온다
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            i = i + 1

        return { 'result' : 'success',
                 'count' : len(result_list),
                  'items' : result_list } 
    
