from flask import Flask  #대문자 주의
from flask_restful import Api # 대문자 주의
from resources.recipe import RecipeListResource
from resources.recipe import RecipeResource

app = Flask(__name__)

api = Api(app)

# 경로와 API동작코드(resource)를 연결한다.
# 경로 : url 의 path 
# ex : http://127.0.0.1:5000/recipes 중 /recipes 가 path

api.add_resource( RecipeListResource , '/recipes' )
api.add_resource( RecipeResource , '/recipes/<int:recipe_id>' ) # <int:recipe_id> 플라스크의 문법

# 폴더생성 : resources, 파일생성 : recipe.py



if __name__ == '__main__' : 
    app.run()

# ctrl+f5 or flask run 하면 flask 서버 실행
# 이 url로 요청이 들어오면 처리해라
