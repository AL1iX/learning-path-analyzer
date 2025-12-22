FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем папку для вывода графиков
RUN mkdir -p output

ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--data", "data/lms_logs.csv"]


