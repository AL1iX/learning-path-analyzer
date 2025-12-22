import argparse
import sys

from src.analyzer import LearningAnalyzer
from src.visualizer import Visualizer

# Принудительная кодировка UTF-8 для вывода в консоль
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Анализатор пути обучения")
    parser.add_argument(
        "--data",
        default="data/lms_logs.csv",
        help="Путь к логам LMS (CSV файл)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Папка для сохранения отчетов и графиков",
    )
    args = parser.parse_args()

    try:
        analyzer = LearningAnalyzer(args.data)
        analyzer.load_data()

        print("=== Анализ пути обучения ===")
        stats = analyzer.get_student_stats()
        print("\nСтатистика по студентам:")
        print(stats)

        corr = analyzer.analyze_correlation()
        print(f"\nКорреляция между активностью и оценками: {corr:.2f}")

        at_risk = analyzer.identify_at_risk()
        if not at_risk.empty:
            print("\n⚠️ ВНИМАНИЕ: Студенты в группе риска (средний балл < 60):")
            print(at_risk[["avg_score", "total_actions"]])
        else:
            print("\nВсе студенты успевают успешно.")

        # Визуализация
        viz = Visualizer(args.output)
        viz.plot_performance(stats)
        viz.plot_correlation(stats)
        print(f"\nГрафики сохранены в папку {args.output}/")

    except Exception as e:
        print(f"Ошибка выполнения: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

