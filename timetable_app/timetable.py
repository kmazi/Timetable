
from .models import TimeSlot


class Timetable(object):
    """
    Generates the timetable for lecturers, levels and department
    """
    def __init__(self, timetable_for=None, lecturer=None, level=None, department=None):
        self.type = timetable_for
        self.lecturer = lecturer
        self.level = level
        self.department = department

    def get_time_slots(self, lecture_times):
        time_slots = dict()
        mon_lectures, tue_lectures = list(), list()
        wed_lectures, thu_lectures = list(), list()
        fri_lectures = list()
        for lecture_time in lecture_times:
            if lecture_time.day.name == "monday":
                mon_lectures.append(lecture_time)
                time_slots["monday"] = mon_lectures
            if lecture_time.day.name == "tuesday":
                tue_lectures.append(lecture_time)
                time_slots["tuesday"] = tue_lectures
            if lecture_time.day.name == "wednesday":
                wed_lectures.append(lecture_time)
                time_slots["wednesday"] = wed_lectures
            if lecture_time.day.name == "thursday":
                thu_lectures.append(lecture_time)
                time_slots["thursday"] = thu_lectures
            if lecture_time.day.name == "friday":
                fri_lectures.append(lecture_time)
                time_slots["friday"] = fri_lectures
        return time_slots

    def generate_timetable(self):
        timetable = dict()
        if self.type == "lecturer":
            time_slots = TimeSlot.objects.filter(course__lecturer=self.lecturer)
        if self.type == "set":
            time_slots = TimeSlot.objects.filter(course__level=self.level,
                                                 course__department__name=self.department)
        if self.type == "department":
            time_slots = TimeSlot.objects.filter(course__department__name=self.department)
        if len(time_slots) > 0:
            timetable = self.get_time_slots(time_slots)
        return timetable
