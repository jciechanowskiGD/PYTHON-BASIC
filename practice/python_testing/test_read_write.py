"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

from python_part_2.task_read_write import extract_vals, save_vals


def test_extract_vals(tmp_path):
    d = tmp_path / "files"
    d.mkdir()
    files = ("f5.txt", "f4.txt", "f1.txt")

    for f in files:
        path = d / f
        path.write_text(f[1])

    assert extract_vals(d) == ["5", "4", "1"]


def test_result_creation(tmp_path):
    f = tmp_path / "result.txt"
    save_vals(f, ["5", "4", "1"])
    assert f.read_text() == "5,4,1"
