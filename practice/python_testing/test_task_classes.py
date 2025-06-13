"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

from python_part_2.task_classes import Homework, Teacher, Student


def test_homework_active():
    homework = Homework("t1", 3)
    assert homework.is_active()


def test_homework_inactive():
    homework = Homework("t1", 0)
    assert not homework.is_active()


def test_homework_nagative():
    homework = Homework("t1", -1)
    assert not homework.is_active()


def test_teacher_creating_homework():
    hw = Teacher.create_homework("A", 1)
    assert issubclass(Homework, hw.__class__)


def test_student_doing_active_homework():
    student = Student("A", "B")
    homework = Homework("t1", 3)
    assert student.do_homework(homework) == homework


def test_student_doing_inactive_homework(capfd):
    student = Student("A", "B")
    homework = Homework("t1", 0)
    assert student.do_homework(homework) == None
    captured = capfd.readouterr()
    assert captured.out == "You are late\n"
