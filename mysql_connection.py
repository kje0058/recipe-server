# 데잍터베이스 연결 전용 파일
# 중요 정보를 분리시켜 관리해야함 

import mysql.connector
from config import Config


def get_connection() : 
    
    connection = mysql.connector.connect(
        host = Config.HOST,
        database = Config.DATABASE,
        user = Config.DB_USER,
        password = Config.DB_PASSWORD
    )
    
    return connection