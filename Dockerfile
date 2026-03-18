FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "-m", "src.main"]
CMD ["--data", "data/lms_logs.csv"]
