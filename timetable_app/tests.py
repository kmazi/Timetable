from django.test import TestCase
from .models import TimeSlot, Day, Course, Department, ClassRoom
from django.contrib.auth.models import User
from datetime import timedelta, time
from .timetable import Timetable


class TimeTableTestCase(TestCase):
    def setUp(self):
        touchstone = User(username="touchstone", password="touchstone1")
        touchstone.save()
        ugo = User(username="ugosko", password="ugosko1")
        ugo.save()
        day = Day.objects.create(name="monday")
        self.lecturer = User.objects.get(username="touchstone")
        self.another_lecturer = User.objects.get(username="ugosko")
        self.department = Department.objects.create(name="systems engineering")
        self.civil_department = Department.objects.create(name="civil engineering")
        self.classroom = ClassRoom.objects.create(name="class 5",
                                             department=self.department,
                                             capacity=100,
                                             type="departmental class")
        self.civil_classroom = ClassRoom.objects.create(name="class 2",
                                                  department=self.civil_department,
                                                  capacity=100,
                                                  type="departmental class")
        self.course = Course.objects.create(code="GEG301",
                                       title="Engineering maths",
                                       department=self.department,
                                       unit=2,
                                       level=300,
                                       lecturer_id=self.lecturer.id)
        self.eng_drawing = Course.objects.create(code="GEG201",
                                            title="Engineering drawing",
                                            department=self.civil_department,
                                            unit=2,
                                            level=200,
                                            lecturer_id=self.another_lecturer.id)
        self.time_slot = TimeSlot(duration=timedelta(hours=1),
                             day=day,
                             start_time=time(11, 0),
                             lecturer=self.lecturer,
                             course=self.course,
                             classroom=self.classroom)
        self.another_time_slot = TimeSlot(duration=timedelta(hours=1),
                                     day=day,
                                     start_time=time(10, 0),
                                     lecturer=self.another_lecturer,
                                     course=self.eng_drawing,
                                     classroom=self.classroom)
        self.another_time_slot.save()
        self.time_slot.save()

    def test_generate_lecturer_timetable(self):
        expected_output = {"monday": [TimeSlot.objects.get(lecturer=self.lecturer)]}
        timetable = Timetable({"timetable_for": "lecturer", "lecturer": self.lecturer})
        actual_output = timetable.generate_timetable()
        self.assertEqual(actual_output, expected_output)

    def test_generate_set_timetable(self):
        TimeSlot.objects.create(duration=timedelta(hours=2),
                                day=Day.objects.create(name="tuesday"),
                                start_time=time(10, 0),
                                lecturer=self.another_lecturer,
                                course=self.eng_drawing,
                                classroom=self.classroom)
        timetable = Timetable({"timetable_for": "set",
                               "level": 100,
                               "department_name": self.department})
        actual_output = timetable.generate_timetable()
        expected_output = {"tuesday":
                           TimeSlot.objects.filter(course__level=200,
                                                   course__department__name="civil engineering")}
        self.assertEqual(actual_output, expected_output)
