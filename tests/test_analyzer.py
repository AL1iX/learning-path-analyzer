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


def test_load_data(sample_csv):
    analyzer = LearningAnalyzer(sample_csv)
    df = analyzer.load_data()
    assert len(df) == 5
    assert "timestamp" in df.columns


def test_student_stats(sample_csv):
    analyzer = LearningAnalyzer(sample_csv)
    analyzer.load_data()
    stats = analyzer.get_student_stats()

    # Студент 1: 2 действия, ср. балл 100
    assert stats.loc[1, "total_actions"] == 2
    assert stats.loc[1, "avg_score"] == 100.0

    # Студент 3: 1 действие, ср. балл 0 (fillna)
    assert stats.loc[3, "avg_score"] == 0.0


def test_at_risk(sample_csv):
    analyzer = LearningAnalyzer(sample_csv)
    analyzer.load_data()
    risky = analyzer.identify_at_risk(score_threshold=60)

    # Студент 2 (50) и Студент 3 (0) должны быть в риске
    assert 2 in risky.index
    assert 3 in risky.index
    assert 1 not in risky.index

