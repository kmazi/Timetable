from django.test import TestCase
from timetable_app.models import TimeSlot, Day, Course, Department, ClassRoom, FreeTime
from django.contrib.auth.models import User
from datetime import timedelta, time
from timetable_app.timetable import Timetable
from timetable_app.lecture import Lecture


class LectureTestCase(TestCase):
    def setUp(self):
        touchstone = User(username="touchstone", password="touchstone1")
        touchstone.save()
        ugo = User(username="ugosko", password="ugosko1")
        ugo.save()
        self.monday = Day.objects.create(name="monday")
        self.tuesday = Day.objects.create(name="tuesday")
        self.wednesday = Day.objects.create(name="wednesday")
        self.thursday = Day.objects.create(name="thursday")
        self.friday = Day.objects.create(name="friday")
        self.lecturer = User.objects.get(username="touchstone")
        self.another_lecturer = User.objects.get(username="ugosko")
        self.fash = User.objects.create(username="fash")
        self.systems_department = Department.objects.create(name="systems engineering")
        self.civil_department = Department.objects.create(name="civil engineering")
        self.classroom = ClassRoom.objects.create(name="class 5",
                                                  department=self.systems_department,
                                                  capacity=100,
                                                  type="departmental class")
        self.sys_classroom = ClassRoom.objects.create(name="class 6",
                                                  department=self.systems_department,
                                                  capacity=100,
                                                  type="departmental class")
        self.gen_classroom = ClassRoom.objects.create(name="civil class",
                                                  department=self.civil_department,
                                                  capacity=70,
                                                  type="departmental class")
        self.civil_classroom = ClassRoom.objects.create(name="class 2",
                                                        department=self.civil_department,
                                                        capacity=100,
                                                        type="departmental class")
        self.maths = Course.objects.create(code="GEG301",
                                            title="Engineering maths",
                                            department=self.systems_department,
                                            unit=2,
                                            level=300,
                                            lecturer=self.lecturer)
        self.control_theory = Course.objects.create(code="SSG202",
                                            title="Control theory 1",
                                            department=self.systems_department,
                                            unit=2,
                                            level=200,
                                            lecturer=self.fash,)
        self.eng_drawing = Course.objects.create(code="CEG201",
                                                 title="Engineering drawing",
                                                 department=self.civil_department,
                                                 unit=2,
                                                 level=200,
                                                 lecturer=self.another_lecturer)
        TimeSlot.objects.create(duration=timedelta(hours=1),
                                  day=self.thursday,
                                  start_time=time(11),
                                  course=self.maths,
                                  classroom=self.classroom)
        TimeSlot.objects.create(duration=timedelta(hours=2),
                                          day=self.monday,
                                          start_time=time(10),
                                          course=self.eng_drawing,
                                          classroom=self.classroom)
        TimeSlot.objects.create(duration=timedelta(hours=1),
                                          day=self.tuesday,
                                          start_time=time(10),
                                          course=self.maths,
                                          classroom=self.classroom)
    
    def test_fix_lecturer_free_time(self):
        lecture = Lecture(self.eng_drawing)
        free_time = FreeTime(available=[8,9,10,11,12,13,14,15,16,17],
                                    day=self.monday,
                                    lecturer=self.another_lecturer)
        lecture.fix_free_time(time(10), timedelta(hours=2), free_time)
        actual_value = FreeTime.objects.get(lecturer=self.another_lecturer, day=self.monday).available
        expected_value = [8,9,12,13,14,15,16,17]
        self.assertEqual(actual_value, expected_value)

    def test_get_common_free_time(self):
        free_time = FreeTime(available=[8,9,11,12,13,14,15,16,17],
                                    day=self.tuesday,
                                    lecturer=self.lecturer)
        lecture = Lecture(self.maths)
        actual_value = lecture.get_common_free_time(free_time.available, self.monday)
        expected_value = [8,9,11,12,13,14,15,16,17]
        self.assertEqual(actual_value, expected_value)

    def test_get_available_classroom(self):
        lecture = Lecture(self.control_theory)
        actual_value = lecture.get_available_classroom(11, self.thursday)
        expected_value = [[], [self.sys_classroom]]
        self.assertEqual(actual_value, expected_value)

    def test_fix_lecture(self):
        lecture = Lecture(self.control_theory)
        lecture.fix_lecture()
        time_slot = list(TimeSlot.objects.filter(course=self.control_theory))
        self.assertTrue(time_slot)