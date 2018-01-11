from django.test import TestCase
from timetable_app.models import TimeSlot, Day, Course, Department, ClassRoom, FreeTime
from django.contrib.auth.models import User
from datetime import timedelta, time
from timetable_app.timetable import Timetable
from timetable_app.lecture import Lecture

class TimeTableTestCase(TestCase):
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
        self.systems_department = Department.objects.create(name="systems engineering")
        self.civil_department = Department.objects.create(name="civil engineering")
        self.classroom = ClassRoom.objects.create(name="class 5",
                                                  department=self.systems_department,
                                                  capacity=100,
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
                                            lecturer=self.lecturer,)
        self.eng_drawing = Course.objects.create(code="GEG201",
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

    def test_generate_lecturer_timetable(self):
        expected_output = {"tuesday": list(TimeSlot.objects.filter(course__lecturer=self.lecturer,
                                                                day__name="tuesday")),
                            "thursday": list(TimeSlot.objects.filter(course__lecturer=self.lecturer,
                                                                day__name="thursday"))}
        timetable = Timetable(timetable_for="lecturer", lecturer=self.lecturer)
        actual_output = timetable.generate_timetable()
        self.assertEqual(actual_output, expected_output)

    def test_generate_set_timetable(self):
        timetable = Timetable(timetable_for="set",
                               level=200,
                               department=self.civil_department.name)
        actual_output = timetable.generate_timetable()
        expected_output = {"monday":
                           list(TimeSlot.objects.filter(course__level=200,
                                                   course__department__name="civil engineering",
                                                   day=self.monday))}
        self.assertEqual(actual_output, expected_output)

    def test_generate_department_timetable(self):
        timetable = Timetable(timetable_for="department",
                               department=self.systems_department.name)
        actual_output = timetable.generate_timetable()
        expected_output = {"tuesday": list(TimeSlot.objects.filter(
                                                            course__department__name="systems engineering",
                                                            day__name="tuesday")
                                                            ),
                            "thursday": list(TimeSlot.objects.filter(course__lecturer=self.lecturer,
                                                                day__name="thursday"))}
        self.assertEqual(actual_output, expected_output)