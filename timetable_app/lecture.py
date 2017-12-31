
from .models import TimeSlot, FreeTime, ClassRoom, Day
from random import randint
from datetime import timedelta, time

class Lecture(object):
    def __init__(self, course):
        self.course = course
        self.department = course.department

    def get_common_free_time(self, lecturer_free_time, day):
        level_fixed_slots = TimeSlot.objects.filter(course__department=self.course.department,
                                                    course__level=self.course.level,
                                                    day=day)
        level_start_times = list()
        if level_fixed_slots.count() > 0:
            for level_fixed_slot in level_fixed_slots:
                level_start_times.append(level_fixed_slot.start_time.hour)
                if level_fixed_slot.duration > timedelta(hours=1):
                    level_start_times.append(level_fixed_slot.start_time.hour + 1)
                
        common_available_time = [common_time for common_time in lecturer_free_time\
            if common_time not in level_start_times]
        return common_available_time

    def get_available_classroom(self, free_start_time, day):
        department_classrooms = ClassRoom.objects.filter(department=self.course.department)
        start_time_query = department_classrooms.exclude(timeslot__start_time=time(free_start_time),
                                                    timeslot__course__department=self.course.department,
                                                    timeslot__day=day)
        free_classroom_at_time = start_time_query.exclude(timeslot__start_time=time(free_start_time-1),
                                        timeslot__duration=timedelta(hours=2))
        classroom_double = list(start_time_query.exclude(timeslot__start_time=time(free_start_time+1)))
        classroom_single = [classroom for classroom in free_classroom_at_time \
        if classroom not in classroom_double]
        return [classroom_single, classroom_double]

    def fix_free_time(self, start_time, duration, free_time):
        affected_start_times = [x for x in range(start_time.hour, start_time.hour + duration.seconds//3600)]
        free_time.available = [val for val in free_time.available if val not in affected_start_times]
        free_time.save()

    def save_lecture_in_database(self,lecture_fix_day, lecture_time, lecture_duration, lecture_fix_classroom, free_time):
        start_time = lecture_time
        duration = lecture_duration
        TimeSlot.objects.create(day=lecture_fix_day,
                                duration=duration,
                                start_time=start_time,
                                course=self.course,
                                classroom=lecture_fix_classroom)
        
        self.fix_free_time(start_time, duration, free_time)

    def fix_lecture(self):
        lecture_fixes = list()
        lecture_fix = dict()
        course_unit = self.course.unit
        days = list(Day.objects.all())
        while course_unit > 0:
            if not len(days):
                break
            lecture_fix["day"] = days[randint(0,len(days)-1)]
            try:
                free_time = FreeTime.objects.get(lecturer=self.course.lecturer,
                                                day=lecture_fix["day"])
            except:
                free_time = FreeTime(available=[8,9,10,11,12,13,14,15,16,17],
                                    day=lecture_fix["day"],
                                    lecturer=self.course.lecturer)
            common_available_time = self.get_common_free_time(free_time.available, lecture_fix["day"])
            lecture_fixed = False
            while lecture_fixed is not True:
                if not len(common_available_time):
                    break
                free_start_time = common_available_time[randint(0, len(common_available_time)-1)]
                lecture_fix["start_time"] = time(free_start_time)
                classroom = self.get_available_classroom(free_start_time, lecture_fix["day"])
                single_classroom = classroom[0]
                double_classroom = classroom[1]
                if free_start_time == 17 or course_unit == 1:
                    lecture_fix["start_time"] = time(free_start_time)
                    lecture_fix["duration"] = timedelta(hours=1)
                    if single_classroom:
                        lecture_fix["classroom"] = single_classroom[randint(0, len(single_classroom)-1)]
                    elif double_classroom:
                        lecture_fix["classroom"] = double_classroom[randint(0, len(double_classroom)-1)]
                    else:
                        common_available_time.remove(free_start_time)
                        continue
                    
                    course_unit -= 1
                    lecture_fixes.append(lecture_fix)
                    self.save_lecture_in_database(lecture_fix["day"], lecture_fix["start_time"], lecture_fix["duration"], lecture_fix["classroom"], free_time)
                    lecture_fixed = True
                else:
                    lecture_fix["start_time"] = time(free_start_time)
                    if double_classroom:
                        lecture_fix["classroom"] = double_classroom[randint(0, len(double_classroom)-1)]
                        lecture_fix["duration"] = timedelta(hours=2)
                        course_unit -= 2
                        lecture_fixes.append(lecture_fix)
                        self.save_lecture_in_database(lecture_fix["day"], lecture_fix["start_time"], lecture_fix["duration"], lecture_fix["classroom"], free_time)
                        lecture_fixed = True
                    elif single_classroom:
                        lecture_fix["classroom"] = single_classroom[randint(0, len(single_classroom)-1)]
                        lecture_fix["duration"] = timedelta(hours=1)
                        course_unit -= 1
                        lecture_fixes.append(lecture_fix)
                        self.save_lecture_in_database(lecture_fix["day"], lecture_fix["start_time"], lecture_fix["duration"], lecture_fix["classroom"], free_time)
                        lecture_fixed = True
                    else:
                        common_available_time.remove(free_start_time)
                        continue
            days.remove(lecture_fix["day"])
        if lecture_fix in lecture_fixes:
            return {"status": "success",
                    "message": "Lecture has been fixed"}
        else:
            return {"status": "fail",
                    "message": "Could not fix lecture for some reasons; maybe there\
                    are no classrooms or free time available"}
