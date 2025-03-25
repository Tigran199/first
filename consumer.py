import redis
import pymysql  #pymysql вместо mysql.connector
import json
import time

# Подключение к Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    try:
        #  pymysql
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="mydatabase",
            ssl={'ssl': False}  # отключение SSL
        )
        
        with db.cursor() as cursor:
            # Чтение сообщения из Redis
            message = r.brpop('messages', timeout=30)
            if message:
                message_data = json.loads(message[1])
                # Запись в MySQL
                cursor.execute("INSERT INTO messages (message) VALUES (%s)", 
                             (message_data['message'],))
                db.commit()
                print(f"Inserted: {message_data['message']}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'db' in locals():
            db.close()
    time.sleep(1)