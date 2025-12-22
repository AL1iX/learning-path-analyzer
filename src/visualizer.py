import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Visualizer:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        import os

        os.makedirs(output_dir, exist_ok=True)

    def plot_performance(self, stats: pd.DataFrame):
        """Строит график успеваемости студентов."""
        plt.figure(figsize=(10, 6))
        sns.barplot(x=stats.index, y=stats["avg_score"], palette="viridis")
        plt.title("Средняя успеваемость студентов")
        plt.xlabel("ID Студента")
        plt.ylabel("Средний балл")
        plt.axhline(y=60, color="r", linestyle="--", label="Порог риска (60)")
        plt.legend()
        plt.savefig(f"{self.output_dir}/performance.png")
        plt.close()

    def plot_correlation(self, stats: pd.DataFrame):
        """Строит график корреляции активности и оценок."""
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=stats["total_actions"], y=stats["avg_score"])
        plt.title("Корреляция: Активность vs Оценка")
        plt.xlabel("Количество действий")
        plt.ylabel("Средний балл")
        plt.savefig(f"{self.output_dir}/correlation.png")
        plt.close()


