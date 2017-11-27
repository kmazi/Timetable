
from .models import TimeSlot, ClassRoom, Day
from random import randint
from datetime import timedelta, time

class Lecture(object):
    def __init__(self, course, department):
        self.course = course
        self.department = department

    def check_available_time(self):
        available_times = list()
        return available_times

    def get_available_classroom(self, given_time, given_duration):
        classrooms = list()
        return classrooms

    def fix_free_time(self, start_time, duration, free_time):
        free_start_times = free_time.available
        affected_start_times = [x in range(start_time.hour, start_time.hour + duration//3600)]
        free_time.available = [val for val in free_start_times if val not in affected_start_times]
        free_time.save()

    def fix_lecture(self):
        lecture_fixes = list()
        lecture_fix = dict()
        course_unit = self.course.unit
        while course_unit > 0:
            lecture_fix["day"] = Day.objects.all()[randint(0,4)]
            try:
                free_time = FreeTime.objects.get(lecturer=self.course.lecturer,
                                                day=lecture_fix["day"])
            expect:
                free_time = FreeTime(available=[8,9,10,11,12,13,14,15,16,17],
                                    day=lecture_fix["day"],
                                    lecturer=self.course.lecturer)
            free_start_times = free_time.available
            free_start_time = free_start_times[randint(0, len(free_start_times)-1)]
            department_time_slot = TimeSlot.objects.filter(course__department=self.course.department,
                                                            start_time=free_start_time)
            before_department_time_slot = TimeSlot.objects.filter(course__department=self.course.department,
                                                            start_time=free_start_time-1)
            after_department_time_slot = TimeSlot.objects.filter(course__department=self.course.department,
                                                            start_time=free_start_time+1)                                                                                              
            booked_slot = department_time_slot.filter(course__level=self.course.level)
            before_booked_slot = before_department_time_slot.filter(course__level=self.course.level)
            after_booked_slot = after_department_time_slot.filter(course__level=self.course.level)
            if booked_slot.count() == 0:
                if before_booked_slot.count() == 0 or \
                before_booked_slot[0].duration == timedelta(hours=1):
                    if after_booked_slot.count() == 0:
                        if free_start_time == 17:
                            lecture_fix["start_time"] = time(free_start_time, 0)
                            lecture_fix["duration"] = timedelta(hours=1)
                            course_unit -= 1
                            lecture_fixes.append(lecture_fix)
                            continue
                        else:
                            lecture_fix["start_time"] = time(free_start_time, 0)
                            set_unit = 2 if course_unit >= 2 else 1
                            lecture_fix["duration"] = timedelta(hours=set_unit)
                            course_unit -= set_unit
                            lecture_fixes.append(lecture_fix)
                            continue
                    else:
                        lecture_fix["start_time"] = time(free_start_time, 0)
                        lecture_fix["duration"] = timedelta(hours=1)
                        course_unit -= 1
                        lecture_fixes.append(lecture_fix)
                        continue
                           
        
        for lecture_fix in lecture_fixes:
            start_time = lecture_fix["start_time"]
            duration = lecture_fix["duration"]
            TimeSlot.objects.create(day=lecture_fix["day"],
                                    duration=lecture_fix["duration"],
                                    start_time=start_time,
                                    lecturer=self.course.lecturer,
                                    course=self.course,
                                    classroom=lecture_fix["classroom"])
            
            self.fix_free_time(start_time, duration, free_time)
