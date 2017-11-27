
from .models import TimeSlot


class Timetable(object):
    """
    Generates the timetable for lecturers, levels and faculty
    """
    def __init__(self, timetable_type):
        self.type = timetable_type

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
        if self.type["timetable_for"] == "lecturer":
            time_slots = TimeSlot.objects.filter(course__lecturer=self.type["lecturer"])
        if self.type["timetable_for"] == "set":
            time_slots = TimeSlot.objects.filter(course__level=self.type["level"],
                                                 course__department__name=self.type["department_name"])
        if self.type["timetable_for"] == "department":
            time_slots = TimeSlot.objects.filter(course__department__name=self.type["department_name"])
        if len(time_slots) > 0:
            timetable = self.get_time_slots(time_slots)
        return timetable
