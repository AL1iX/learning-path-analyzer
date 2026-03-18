import logging
import os
from typing import Optional

import pandas as pd

REQUIRED_COLUMNS = {"student_id", "timestamp", "event_type", "score"}

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LearningAnalyzer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.df: Optional[pd.DataFrame] = None
        self._stats: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Загружает и подготавливает данные логов."""
        if not os.path.exists(self.data_path):
            logger.error(f"Файл {self.data_path} не найден")
            raise FileNotFoundError(f"Файл {self.data_path} не найден")

        logger.info(f"Загрузка данных из {self.data_path}")
        self.df = pd.read_csv(self.data_path)

        missing = REQUIRED_COLUMNS - set(self.df.columns)
        if missing:
            raise ValueError(f"В CSV отсутствуют обязательные колонки: {missing}")

        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])
        self._stats = None
        return self.df

    def get_student_stats(self) -> pd.DataFrame:
        """Агрегирует статистику по студентам (с кэшированием)."""
        if self.df is None:
            logger.error("Попытка агрегации без загруженных данных")
            raise ValueError("Данные не загружены")

        if self._stats is not None:
            return self._stats

        scored = self.df.dropna(subset=["score"])

        stats = self.df.groupby("student_id").agg(
            total_actions=("event_type", "count"),
            last_active=("timestamp", "max"),
        )

        if not scored.empty:
            avg_scores = scored.groupby("student_id")["score"].mean()
            stats["avg_score"] = avg_scores
        else:
            stats["avg_score"] = pd.NA

        stats["has_scores"] = stats["avg_score"].notna()

        self._stats = stats.sort_values(
            "avg_score", ascending=False, na_position="last"
        )
        return self._stats

    def analyze_correlation(self) -> Optional[float]:
        """Вычисляет корреляцию между активностью и успеваемостью.

        Учитывает только студентов, у которых есть хотя бы одна оценка.
        Возвращает None, если недостаточно данных для расчета.
        """
        stats = self.get_student_stats()
        scored_stats = stats[stats["has_scores"]]

        if len(scored_stats) < 3:
            logger.warning(
                f"Недостаточно данных для корреляции "
                f"(студентов с оценками: {len(scored_stats)}, нужно >= 3)"
            )
            return None

        correlation = scored_stats["total_actions"].corr(scored_stats["avg_score"])
        logger.info(f"Корреляция (Активность vs Оценка): {correlation:.2f}")
        return correlation

    def identify_at_risk(self, score_threshold: float = 60.0) -> pd.DataFrame:
        """Определяет студентов в группе риска.

        Включает студентов с низким баллом И студентов без единой оценки.
        """
        stats = self.get_student_stats()
        low_score = stats[stats["has_scores"] & (stats["avg_score"] < score_threshold)]
        no_scores = stats[~stats["has_scores"]]

        at_risk = pd.concat([low_score, no_scores])
        logger.info(f"Найдено {len(at_risk)} студентов в группе риска")
        return at_risk
