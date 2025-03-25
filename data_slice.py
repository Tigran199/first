import pymysql
import time
from datetime import datetime

# Настройки подключения
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'mydatabase',
    'ssl': False  # отключаем SSL
}

def fetch_data():
    conn = pymysql.connect(**config)
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM messages")
        return cursor.fetchall()

def save_to_file(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"data_slice_{timestamp}.txt", 'w') as f:
        for row in data:
            f.write(','.join(map(str, row)) + '\n')

if __name__ == "__main__":
    while True:
        try:
            data = fetch_data()
            save_to_file(data)
            time.sleep(300)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)