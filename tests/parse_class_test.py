import pytest
from src.app.main import ParseCSV
from pathlib import Path


@pytest.fixture
def csv_file(tmp_path):
    content = (
        "name,hours_worked,hourly_rate,department\n"
        "Alice,8,20,IT\n"
        "Bob,10,15,HR"
    )
    file = tmp_path / "test_data.csv"
    file.write_text(content)
    return file.name, tmp_path


def test_parse_csv(csv_file):
    filename, base_dir = csv_file
    parser = ParseCSV([filename], base_dir=base_dir)
    parser.parse_csv()

    data = parser.__dict__()
    assert filename in data
    assert data[filename][0]["name"] == "Alice"
    assert data[filename][1]["hours_worked"] == "10"


def test_get_result_with_payout_report(csv_file):
    filename, base_dir = csv_file
    parser = ParseCSV([filename], report="payout", base_dir=base_dir)
    parser.parse_csv()
    result = parser.get_result()

    assert "Alice" in result
    assert "Bob" in result
    assert "160" in result
    assert "150" in result
    assert "IT" in result
    assert "HR" in result


def test_missing_salary_field(tmp_path):
    file = tmp_path / "invalid.csv"
    file.write_text("name,hours_worked,department\nEve,5,QA")
    parser = ParseCSV([file.name], report="payout", base_dir=tmp_path)
    parser.parse_csv()

    with pytest.raises(ValueError, match="Not found salary"):
        parser.get_result()


def test_file_not_found(capfd):
    parser = ParseCSV(["nonexistent.csv"], base_dir=Path.cwd())
    parser.parse_csv()
    out, _ = capfd.readouterr()
    assert "not found" in out.lower()
