import csv
import random
from datetime import datetime, timedelta

SEED = 42
EVENTS = ["login", "view_material", "quiz_attempt", "forum_post", "submit_assignment"]
MATERIALS = {
    "view_material": ["lecture_1", "lecture_2", "lecture_3"],
    "quiz_attempt": ["quiz_1", "quiz_2"],
    "submit_assignment": ["assign_1", "assign_2"],
    "forum_post": ["topic_1", "topic_2"],
}


def generate_logs(filename="data/generated_logs.csv", num_records=100, seed=SEED):
    """Генерирует воспроизводимые логи для тестирования системы."""
    random.seed(seed)
    student_ids = range(101, 111)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["student_id", "timestamp", "event_type", "material_id", "score"]
        )

        start_date = datetime(2023, 9, 1)

        for _ in range(num_records):
            stu_id = random.choice(student_ids)
            event = random.choice(EVENTS)

            timestamp = start_date + timedelta(
                days=random.randint(0, 30),
                hours=random.randint(8, 20),
                minutes=random.randint(0, 59),
            )

            material_id = ""
            if event in MATERIALS:
                material_id = random.choice(MATERIALS[event])

            score = ""
            if event in ("quiz_attempt", "submit_assignment"):
                score = random.randint(40, 100)

            writer.writerow([stu_id, timestamp, event, material_id, score])

    print(f"Сгенерировано {num_records} записей в {filename}")


if __name__ == "__main__":
    import os

    os.makedirs("data", exist_ok=True)
    generate_logs()
