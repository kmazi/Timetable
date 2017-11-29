
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

    def get_available_classroom(self, free_start_time, day, duration=1):
        free_classrooms = ClassRoom.objects.exclude(timeslot__day=day,
                                    timeslot__course__department=self.course.department)
        free_classroom_at_time = ClassRoom.objects.exclude(timeslot__start_time=free_start_time,
                                                    timeslot__course__department=self.course.department,
                                                    timeslot__day=day)
        free_classrooms_bf_time = ClassRoom.objects.exclude(timeslot__start_time=free_start_time-1,
                                                    timeslot__course__department=self.course.department,
                                                    timeslot__day=day,
                                                    timeslot__course__unit__gte=2)
        free_classrooms_af_time = ClassRoom.objects.exclude(timeslot__start_time=free_start_time+1,
                                                    timeslot__course__department=self.course.department,
                                                    timeslot__day=day,
                                                    timeslot__course__unit__gte=2)
        all_department_classrooms = ClassRoom.objects.all()
        if duration == 1:
            return [{"classrooms": free_classroom_at_time, "duration": 2} for \
            free_classroom in free_classroom_at_time]
        if free_classrooms:
            return [{"classrooms": free_classroom, "duration": 2} for \
            free_classroom in free_classrooms]
        else:
            free_classrooms = [classroom for classroom in all_department_classrooms \
                                if classroom.name not in busy_classrooms]
            return free_classrooms

    def fix_free_time(self, start_time, duration, free_time):
        free_lecturer_start_times = free_time.available
        affected_start_times = [x in range(start_time.hour, start_time.hour + duration//3600)]
        free_time.available = [val for val in free_lecturer_start_times if val not in affected_start_times]
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
            free_lecturer_start_times = free_time.available
            level_fixed_slots = TimeSlot.objects.filter(course__department=self.course.department,
                                                            course__level=self.course.level,
                                                            day=lecture_fix["day"])
            level_start_times = list()
            if level_fixed_slots.count() > 0:
                for level_fixed_slot in level_fixed_slots:
                    level_start_times.append(level_fixed_slot.start_time.hour)
                    if level_fixed_slot.duration > timedelta(hours=1):
                        level_start_times.append(level_fixed_slot.start_time.hour + 1)
                    
            common_available_time = [common_time for common_time in free_lecturer_start_times\
             if common_time not in level_start_times]

            lecture_fixed = False
            while lecture_fixed not True:
                if len(common_available_time):
                    break
                free_start_time = common_available_time[randint(0, len(common_available_time)-1)]
                lecture_fix["start_time"] = time(free_start_time, 0)
                if free_start_time == 17 or course_unit == 1:
                    lecture_fix["start_time"] = time(free_start_time, 0)
                    lecture_fix["duration"] = timedelta(hours=1)
                    classroom = self.get_available_classroom(free_start_time, lecture_fix["day"])
                    if classroom:
                        lecture_fix["classroom"] = classroom[0]["classroom"]
                    else:
                        index = common_available_time.index(free_start_time)
                        common_available_time.pop(index)
                        continue
                    
                    course_unit -= 1
                    lecture_fixes.append(lecture_fix)
                    lecture_fixed = True
                else:
                    lecture_fix["start_time"] = time(free_start_time, 0)
                    classroom = self.get_available_classroom(free_start_time, lecture_fix["day"], 2)
                    if classroom:
                        lecture_fix["classroom"] = classroom[0]["classroom"]
                        lecture_fix["duration"] = timedelta(hours=2)
                        course_unit -= 2
                        lecture_fixes.append(lecture_fix)
                        lecture_fixed = True
                        continue
                    else:
                        classroom = self.get_available_classroom(free_start_time, lecture_fix["day"])
                        if classroom:
                            lecture_fix["classroom"] = classroom[0]["classroom"]
                        else:
                            index = common_available_time.index(free_start_time)
                            common_available_time.pop(index)
                            continue
                        lecture_fix["duration"] = timedelta(hours=1)
                        course_unit -= 1
                        lecture_fixes.append(lecture_fix)
                        lecture_fixed = True
        
        for lecture_fix in lecture_fixes:
            start_time = lecture_fix["start_time"]
            duration = lecture_fix["duration"]
            TimeSlot.objects.create(day=lecture_fix["day"],
                                    duration=lecture_fix["duration"],
                                    start_time=start_time,
                                    lecturer=self.course.lecturer,
                                    course=self.course,
                                    classroom=lecture_fix["classroom"])
            
            self.fix_free_time(start_time, duration.seconds, free_time)
