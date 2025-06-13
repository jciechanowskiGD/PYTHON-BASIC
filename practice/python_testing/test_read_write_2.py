"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

from python_part_2.task_read_write_2 import save, generate_words


def test_generate_words():
    words = generate_words()

    assert issubclass(list, words.__class__)


def test_saving(tmp_path):
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    save(["aaa", "441", "222", "xa2s"], (f1, f2), ("utf-8", "cp1252"))
    assert f1.read_text(encoding="utf-8") == "aaa\n441\n222\nxa2s"
    assert f2.read_text(encoding="cp1252") == "aaa\n441\n222\nxa2s"
