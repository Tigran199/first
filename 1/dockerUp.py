import csv
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="forum_user",
    password="forum_pass",
    database="forum_logs"
)

cursor = conn.cursor()

with open('logs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute("""
            INSERT INTO logs (user_id, action, target_id, status, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            int(row['user_id']) if row['user_id'] else None,
            row['action'],
            int(row['target_id']) if row['target_id'] else None,
            row['status'],
            row['timestamp']
        ))

conn.commit()
cursor.close()
conn.close()

print("Данные загружены в базу.")
