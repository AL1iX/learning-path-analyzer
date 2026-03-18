import os

import pytest

from src.analyzer import LearningAnalyzer


@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "test_logs.csv"
    data = """student_id,timestamp,event_type,material_id,score
1,2023-01-01 10:00,login,,
1,2023-01-01 10:05,quiz,q1,100
2,2023-01-01 10:00,login,,
2,2023-01-01 10:05,quiz,q1,50
3,2023-01-01 10:00,login,,
"""
    csv_file.write_text(data, encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def analyzer(sample_csv):
    a = LearningAnalyzer(sample_csv)
    a.load_data()
    return a


def test_load_data(sample_csv):
    a = LearningAnalyzer(sample_csv)
    df = a.load_data()
    assert len(df) == 5
    assert "timestamp" in df.columns


def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        LearningAnalyzer("nonexistent.csv").load_data()


def test_load_invalid_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("col_a,col_b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="обязательные колонки"):
        LearningAnalyzer(str(bad_csv)).load_data()


def test_student_stats(analyzer):
    stats = analyzer.get_student_stats()

    assert stats.loc[1, "total_actions"] == 2
    assert stats.loc[1, "avg_score"] == 100.0
    assert stats.loc[2, "avg_score"] == 50.0

    assert not stats.loc[3, "has_scores"]
    assert str(stats.loc[3, "avg_score"]) == "nan"


def test_stats_caching(analyzer):
    stats1 = analyzer.get_student_stats()
    stats2 = analyzer.get_student_stats()
    assert stats1 is stats2


def test_at_risk(analyzer):
    risky = analyzer.identify_at_risk(score_threshold=60)

    assert 2 in risky.index
    assert 3 in risky.index
    assert 1 not in risky.index


def test_correlation(analyzer):
    corr = analyzer.analyze_correlation()
    assert corr is None


def test_correlation_enough_data(tmp_path):
    csv_file = tmp_path / "big.csv"
    data = """student_id,timestamp,event_type,material_id,score
1,2023-01-01 10:00,login,,
1,2023-01-01 10:05,quiz,q1,90
2,2023-01-01 10:00,login,,
2,2023-01-01 10:05,quiz,q1,70
2,2023-01-01 10:10,quiz,q2,80
3,2023-01-01 10:00,quiz,q1,50
"""
    csv_file.write_text(data, encoding="utf-8")
    a = LearningAnalyzer(str(csv_file))
    a.load_data()
    corr = a.analyze_correlation()
    assert corr is not None
    assert -1.0 <= corr <= 1.0


def test_stats_without_load():
    a = LearningAnalyzer("dummy.csv")
    with pytest.raises(ValueError, match="не загружены"):
        a.get_student_stats()


class TestMain:
    def test_main_success(self, tmp_path, sample_csv):
        import sys

        from src.main import main

        out = str(tmp_path / "report")
        original_argv = sys.argv
        sys.argv = ["prog", "--data", sample_csv, "--output", out]
        try:
            code = main()
        finally:
            sys.argv = original_argv
        assert code == 0
        assert os.path.isfile(os.path.join(out, "performance.png"))

    def test_main_missing_file(self):
        import sys

        from src.main import main

        original_argv = sys.argv
        sys.argv = ["prog", "--data", "no_such_file.csv"]
        try:
            code = main()
        finally:
            sys.argv = original_argv
        assert code == 1


class TestVisualizer:
    def test_creates_output_dir(self, tmp_path):
        from src.visualizer import Visualizer

        out = str(tmp_path / "charts")
        Visualizer(out)
        assert os.path.isdir(out)

    def test_generates_plots(self, tmp_path, analyzer):
        from src.visualizer import Visualizer

        out = str(tmp_path / "plots")
        stats = analyzer.get_student_stats()
        scored = stats[stats["has_scores"]]

        viz = Visualizer(out)
        viz.plot_performance(scored)
        viz.plot_correlation(scored)

        assert os.path.isfile(os.path.join(out, "performance.png"))
        assert os.path.isfile(os.path.join(out, "correlation.png"))
