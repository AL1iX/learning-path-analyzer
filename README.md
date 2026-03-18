# Learning Path Analyzer 📊

![CI/CD](https://github.com/al1ix/learning-path-analyzer/actions/workflows/analysis.yml/badge.svg)

Система анализа пути обучения студента на основе логов LMS (Learning Management System). Проект анализирует корреляцию между активностью студентов и их успеваемостью, выявляет студентов в "группе риска" и визуализирует данные.

**Автор:** Шакиров Салават (@al1ix)  
**Проект:** 1.1 Learning Path Analyzer (Категория: Образовательная аналитика)

## 📋 Функционал

- **Парсинг логов:** Обработка CSV-файлов с действиями студентов (login, quiz, forum).
- **Аналитика:** Расчет корреляции между активностью и оценками.
- **Risk Detection:** Автоматическое выявление отстающих студентов.
- **Визуализация:** Генерация графиков успеваемости и активности.
- **CI/CD:** Автоматическое тестирование и анализ данных при каждом пуше.

## 🛠️ Установка

**Требования:** Python 3.9+

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/AL1iX/learning-path-analyzer.git
   cd learning-path-analyzer
   ```

2. (Рекомендуется) Создайте виртуальное окружение:

   ```bash
   python -m venv venv
   # Linux/macOS:
   source venv/bin/activate
   # Windows (PowerShell):
   venv\Scripts\Activate.ps1
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Использование

### Анализ данных

```bash
python -m src.main --data data/lms_logs.csv
```

**Результат:**

- В консоль выводится статистика и корреляция.
- В папке `output/` создаются графики:
  - `performance.png`: Успеваемость студентов.
  - `correlation.png`: Зависимость оценки от активности.

Пример вывода в консоль:

```text
=== Анализ пути обучения ===

Статистика по студентам:
            total_actions  avg_score         last_active
student_id
101                     6       90.0 2023-09-02 09:45:00
...

Корреляция между активностью и оценками: 0.93

⚠️ ВНИМАНИЕ: Студенты в группе риска (средний балл < 60):
            avg_score  total_actions
student_id
104              40.0              2

Графики сохранены в папку output/
```

### Запуск тестов

```bash
pytest --cov=src
```

### Проверка качества кода (PEP8/format/imports)

```bash
flake8 src tests
black --check src tests
isort --check-only src tests
```

Автоформатирование:

```bash
black src tests
isort src tests
```

### Docker

```bash
docker build -t lms-analyzer .
# Linux/macOS (bash):
docker run --rm -v $(pwd)/output:/app/output lms-analyzer
```

Windows (PowerShell):

```bash
docker run --rm -v ${PWD}/output:/app/output lms-analyzer
```

## 📁 Структура проекта

```
learning-path-analyzer/
├── .dockerignore         # Исключения для Docker-образа
├── .flake8               # Настройки flake8
├── .github/workflows/    # CI/CD конфигурация
├── .gitignore            # Исключения для git (кэш, артефакты и т.п.)
├── data/                 # Данные логов
├── requirements.txt      # Зависимости проекта
├── scripts/              # Скрипты генерации данных
├── src/                  # Исходный код
│   ├── analyzer.py       # Логика анализа
│   ├── visualizer.py     # Визуализация
│   └── main.py           # Точка входа
├── tests/                # Тесты
├── Dockerfile            # Конфигурация Docker
└── README.md             # Документация
```

Примечание для Windows: папка `.github/` может быть не видна в проводнике, если отключено отображение скрытых/системных файлов.

## 📁 Формат данных

Входной файл `lms_logs.csv` должен содержать:

- `student_id`: ID студента
- `timestamp`: Время события
- `event_type`: Тип события (login, quiz_attempt, etc.)
- `score`: Оценка (опционально)

## 🤖 CI/CD

Проект использует **GitHub Actions** для:

1. Автоматического тестирования и проверок качества кода (Pytest, Flake8, Black, isort).
2. Запуска анализа данных при каждом push/PR.
3. Сохранения отчетов и графиков в Artifacts.

Где смотреть результаты:

- **Actions → последний запуск workflow → Artifacts**: архив `analysis-report` (папка `report_output/`).

## 📄 Лицензия

Творческое задание по программированию (15 баллов).
