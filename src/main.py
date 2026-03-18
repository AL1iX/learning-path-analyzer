import argparse
import logging
import sys

from src.analyzer import LearningAnalyzer
from src.visualizer import Visualizer

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

logger = logging.getLogger(__name__)


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
        if corr is not None:
            print(f"\nКорреляция между активностью и оценками: {corr:.2f}")
        else:
            print("\nНедостаточно данных для расчёта корреляции.")

        at_risk = analyzer.identify_at_risk()
        if not at_risk.empty:
            print("\n⚠️ ВНИМАНИЕ: Студенты в группе риска (средний балл < 60):")
            scored_risk = at_risk[at_risk["has_scores"]]
            unscored_risk = at_risk[~at_risk["has_scores"]]
            if not scored_risk.empty:
                print("  Низкий балл:")
                print(scored_risk[["avg_score", "total_actions"]])
            if not unscored_risk.empty:
                print("  Нет ни одной оценки:")
                print(unscored_risk[["total_actions"]])
        else:
            print("\nВсе студенты успевают успешно.")

        scored_stats = stats[stats["has_scores"]]
        viz = Visualizer(args.output)
        viz.plot_performance(scored_stats)
        viz.plot_correlation(scored_stats)
        print(f"\nГрафики сохранены в папку {args.output}/")

    except (FileNotFoundError, ValueError) as e:
        print(f"Ошибка входных данных: {e}")
        return 1
    except Exception:
        logger.exception("Непредвиденная ошибка")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
