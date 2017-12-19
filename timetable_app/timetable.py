from datetime import timedelta
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
        new_slots = dict()
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
        for day, time_slot in time_slots.items():
            i = 0
            lectures = list()
            next_count = 8
            for count in range(8, 18):
                length = len(time_slot)
                if length > i and time_slot[i].start_time.hour == count:
                    lectures.append(time_slot[i])
                    if time_slot[i].duration == timedelta(hours=2):
                        next_count += 2
                    i+=1
                else:
                    if next_count == count:
                        lectures.append("")
                        next_count += 1
            new_slots[day] = lectures
        return new_slots

    def generate_timetable(self):
        timetable = dict()
        if self.type == "lecturer":
            time_slots = TimeSlot.objects.filter(course__lecturer=self.lecturer)\
                                              .order_by('day', 'start_time')
        if self.type == "set":
            time_slots = TimeSlot.objects.filter(course__level=self.level,
                                                 course__department__name=self.department)\
                                                 .order_by('day', 'start_time')
        if self.type == "department":
            time_slots = TimeSlot.objects.filter(course__department__name=self.department)\
                                                .order_by('day', 'start_time')
        if len(time_slots) > 0:
            timetable = self.get_time_slots(time_slots)
        return timetable
