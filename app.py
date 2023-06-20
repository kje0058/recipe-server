from flask import Flask  #대문자 주의
from flask_restful import Api
from config import Config # 대문자 주의
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource, MyRecipeListResource
from resources.user import UserRegisterResource, UserLoginResource, UserLogoutResource, jwt_blocklist
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# 환경변수 셋팅
app.config.from_object(Config)

# JWT 매니저 초기화
jwt = JWTManager(app)
# Flask-JWT-Extended 확장에 대한 JWT 설정 및 콜백 기능을 보유하는 데 사용되는 개체

# 로그아웃된 토큰으로 요청하는 경우!
# 이 경우는 비정상적인 경우 이므로 JWT가 알아서 처리하도록 코드작성
@jwt.token_in_blocklist_loader # 블락리스트에 있는 토큰 관리하겠다
def check_if_token_is_revoked( jwt_header, jwt_payload ) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist


api = Api(app)

# 경로와 API동작코드(resource)를 연결한다.
# 경로 : url 의 path 
# ex : http://127.0.0.1:5000/recipes 중 /recipes 가 path

api.add_resource( RecipeListResource , '/recipes' )
api.add_resource( RecipeResource , '/recipes/<int:recipe_id>' ) # <int:recipe_id> 플라스크의 문법
api.add_resource( UserRegisterResource , '/user/register') # 만약 api가 없으면 생성해줄것
api.add_resource( UserLoginResource , '/user/login')
api.add_resource( UserLogoutResource, '/user/logout' )
api.add_resource( RecipePublishResource, '/recipes/<int:recipe_id>/publish' ) # 공개, 임시저장 둘다 put delete 이용
api.add_resource( MyRecipeListResource, '/recipes/me' )
# 폴더생성 : resources, 파일생성 : recipe.py

if __name__ == '__main__' : 
    app.run()

# ctrl+f5 or flask run 하면 flask 서버 실행
# 이 url로 요청이 들어오면 처리해라
