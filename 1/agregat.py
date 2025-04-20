import mysql.connector
import csv
from datetime import datetime, timedelta
import sys

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="forum_user",
        password="forum_pass",
        database="forum_logs"
    )

def aggregate_logs(start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    current_date = start_date
    results = []

    previous_topic_count = 0

    while current_date <= end_date:
        next_day = current_date + timedelta(days=1)

        cursor.execute("""
            SELECT COUNT(*) AS count FROM logs
            WHERE action = 'register'
            AND timestamp >= %s AND timestamp < %s
        """, (current_date, next_day))
        new_accounts = cursor.fetchone()['count']

        cursor.execute("""
            SELECT 
                SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS anon_messages,
                COUNT(*) AS total_messages
            FROM logs
            WHERE action = 'write_message'
            AND timestamp >= %s AND timestamp < %s
        """, (current_date, next_day))
        row = cursor.fetchone()
        total_messages = row['total_messages'] or 0
        anon_messages = row['anon_messages'] or 0

        cursor.execute("""
            SELECT COUNT(*) AS count FROM logs
            WHERE action = 'create_topic'
            AND status = 'success'
            AND timestamp <= %s
        """, (next_day,))
        topic_count = cursor.fetchone()['count']

        anon_percent = (anon_messages / total_messages * 100) if total_messages else 0
        topic_growth = ((topic_count - previous_topic_count) / previous_topic_count * 100) if previous_topic_count else 0

        results.append({
            'day': current_date.strftime('%Y-%m-%d'),
            'new_accounts': new_accounts,
            'anon_message_percent': round(anon_percent, 2),
            'total_messages': total_messages,
            'topic_growth_percent': round(topic_growth, 2)
        })

        previous_topic_count = topic_count
        current_date = next_day

    cursor.close()
    conn.close()

    return results

def save_to_csv(data, filename='aggregated_report.csv'):
    with open(filename, mode='w', newline='') as file:
        fieldnames = ['day', 'new_accounts', 'anon_message_percent', 'total_messages', 'topic_growth_percent']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    start = sys.argv[1] if len(sys.argv) > 2 else '2025-04-01'
    end = sys.argv[2] if len(sys.argv) > 2 else '2025-04-30'

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    aggregated_data = aggregate_logs(start_date, end_date)
    save_to_csv(aggregated_data)

    print(f"Файл 'aggregated_report.csv' успешно создан с данными за период: {start} — {end}")
