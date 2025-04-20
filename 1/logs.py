import random
import csv
from datetime import datetime, timedelta

ACTIONS = [
    'visit_site', 'register', 'login', 'logout',
    'create_topic', 'view_topic', 'delete_topic', 'write_message'
]

USERS = [i for i in range(1, 101)] 
TOPIC_ID = 1  

def generate_logs_for_day(date):
    global TOPIC_ID
    logs = []

    def log_entry(user_id, action, target_id, status):
        return {
            'user_id': user_id,
            'action': action,
            'target_id': target_id,
            'status': status,
            'timestamp': datetime.combine(date, datetime.min.time()) + timedelta(
                seconds=random.randint(0, 86399)
            )
        }

    for action in ACTIONS:
        for _ in range(5):
            user_id = random.choice(USERS) if action != 'write_message' or random.random() < 0.5 else None
            target_id = None
            status = 'success'

            if action == 'create_topic':
                if len([l for l in logs if l['action'] == 'create_topic' and l['status'] == 'error']) < 2:
                    if random.random() < 0.5:
                        user_id = None
                        status = 'error'
                    else:
                        user_id = random.choice(USERS)
                        target_id = TOPIC_ID
                        TOPIC_ID += 1
                else:
                    user_id = random.choice(USERS)
                    target_id = TOPIC_ID
                    TOPIC_ID += 1

            elif action == 'write_message':
                target_id = random.randint(1, max(1, TOPIC_ID - 1))

            elif action in ('view_topic', 'delete_topic'):
                target_id = random.randint(1, max(1, TOPIC_ID - 1))

            logs.append(log_entry(user_id, action, target_id, status))

    extra_actions = random.randint(20, 50)
    for _ in range(extra_actions):
        action = random.choice(ACTIONS)
        user_id = random.choice(USERS) if action != 'write_message' or random.random() < 0.5 else None
        target_id = None
        status = 'success'

        if action == 'create_topic':
            if random.random() < 0.2:
                user_id = None
                status = 'error'
            else:
                user_id = random.choice(USERS)
                target_id = TOPIC_ID
                TOPIC_ID += 1

        elif action == 'write_message':
            target_id = random.randint(1, max(1, TOPIC_ID - 1))

        elif action in ('view_topic', 'delete_topic'):
            target_id = random.randint(1, max(1, TOPIC_ID - 1))

        logs.append(log_entry(user_id, action, target_id, status))

    return logs


def generate_month(start_date):
    dataset = []
    for day in range(30):
        date = start_date + timedelta(days=day)
        dataset.extend(generate_logs_for_day(date))
    return dataset


def save_logs_to_csv(logs, filename='logs.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'action', 'target_id', 'status', 'timestamp'])
        writer.writeheader()
        for row in logs:
            row['timestamp'] = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow(row)


if __name__ == '__main__':
    start_date = datetime(2025, 4, 1) 
    logs = generate_month(start_date)
    save_logs_to_csv(logs)
    print(f'Логи успешно сгенерированы: {len(logs)} строк записано в logs.csv')
