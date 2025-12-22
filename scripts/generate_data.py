import csv
import random
from datetime import datetime, timedelta


def generate_logs(filename="data/generated_logs.csv", num_records=100):
    """Генерирует случайные логи для тестирования системы."""
    events = ["login", "view_material", "quiz_attempt", "forum_post", "submit_assignment"]
    student_ids = range(101, 111)  # 10 студентов

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "timestamp", "event_type", "material_id", "score"])

        start_date = datetime(2023, 9, 1)

        for _ in range(num_records):
            stu_id = random.choice(student_ids)
            event = random.choice(events)

            # Случайное время
            timestamp = start_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(8, 20),
                minutes=random.randint(0, 59),
            )

            score = ""
            if event in ["quiz_attempt", "submit_assignment"]:
                score = random.randint(40, 100)

            writer.writerow([stu_id, timestamp, event, "", score])

    print(f"Сгенерировано {num_records} записей в {filename}")


if __name__ == "__main__":
    import os

    os.makedirs("data", exist_ok=True)
    generate_logs()


