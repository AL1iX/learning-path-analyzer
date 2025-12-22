import logging
import os
from typing import Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LearningAnalyzer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Загружает и подготавливает данные логов."""
        if not os.path.exists(self.data_path):
            logger.error(f"Файл {self.data_path} не найден")
            raise FileNotFoundError(f"Файл {self.data_path} не найден")

        logger.info(f"Загрузка данных из {self.data_path}")
        self.df = pd.read_csv(self.data_path)
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        return self.df

    def get_student_stats(self) -> pd.DataFrame:
        """Агрегирует статистику по студентам."""
        if self.df is None:
            logger.error("Попытка агрегации без загруженных данных")
            raise ValueError("Данные не загружены")

        stats = self.df.groupby("student_id").agg(
            total_actions=("event_type", "count"),
            avg_score=("score", "mean"),
            last_active=("timestamp", "max"),
        )
        # Заполняем пропуски в оценках нулями (если студент ничего не сдавал)
        stats["avg_score"] = stats["avg_score"].fillna(0)
        return stats.sort_values("avg_score", ascending=False)

    def analyze_correlation(self) -> float:
        """Вычисляет корреляцию между активностью и успеваемостью."""
        stats = self.get_student_stats()
        correlation = stats["total_actions"].corr(stats["avg_score"])
        logger.info(f"Корреляция (Активность vs Оценка): {correlation:.2f}")
        return correlation

    def identify_at_risk(self, score_threshold: float = 60.0) -> pd.DataFrame:
        """Определяет студентов в группе риска."""
        stats = self.get_student_stats()
        at_risk = stats[stats["avg_score"] < score_threshold]
        logger.info(f"Найдено {len(at_risk)} студентов в группе риска")
        return at_risk

