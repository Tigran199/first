import pymysql
import csv

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1z2z3f4f',
    database='history',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.Cursor
)

cursor = conn.cursor()

query = "SELECT * FROM history_participant"
cursor.execute(query)
rows = cursor.fetchall()

transformed = [(row[0], row[1].upper(), row[2], row[3], row[4]) for row in rows]

with open('history_participant_transformed.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['id_participant', 'name', 'date_birth', 'date_death', 'description'])
    writer.writerows(transformed)

print("Данные успешно выгружены в history_participant_transformed.csv")

cursor.close()
conn.close()
