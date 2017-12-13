from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta


class Department(models.Model):
    class Meta:
        db_table = "Department"
    name = models.CharField(max_length=100, help_text="Enter a valid department name", unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    the profile of every user
    """
    class Meta:
        db_table = "UserProfile"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_OPTIONS = (('male', 'male'), ('female', 'female'), ('others', 'others'))
    gender = models.CharField(max_length=6, choices=GENDER_OPTIONS)
    department = models.ForeignKey(Department,
                                   on_delete=models.CASCADE)
    break_time_start = models.TimeField(null=True, blank=True)
    break_time_duration = models.DurationField(default=timedelta(hours=1))

    def __str__(self):
        """
        the string representation of the user profile class
        :return: returns the name of the user
        """
        return self.user.username


class ClassRoom(models.Model):
    class Meta:
        db_table = "ClassRoom"
    name = models.CharField(max_length=100, help_text="Enter a name for the classroom", unique=True)
    department = models.ForeignKey(Department, help_text="Select an existing department", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField(help_text="Enter a capacity for the classroom")
    CLASS_TYPES = (("laboratory", "Laboratory"), ("lecture hall", "Lecture Hall"),
                   ("departmental class", "Departmental Class"))
    type = models.CharField(max_length=50,
                            help_text="Enter a classroom type e.g lag",
                            choices=CLASS_TYPES)

    def __str__(self):
        return "{0} in {1}".format(self.name, self.department)

    def get_absolute_url(self):
        """
            Returns the url to access a particular classroom instance.
        """
        return reverse('classroom-detail', args=[str(self.id)])


class Course(models.Model):
    class Meta:
        db_table = 'Course'
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    unit = models.PositiveSmallIntegerField()
    LEVELS = ((100, 100), (200, 200), (300, 300), (400, 400), (500, 500),
              (600, 600))
    level = models.PositiveSmallIntegerField(help_text="Enter a level for the course",
                                             choices=LEVELS)
    lecturer = models.ForeignKey(User, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.code, self.title)

    def lecture_fixed(self):
        time_slots = TimeSlot.objects.filter(course__code=self.code)
        if len(list(time_slots)):
            return True
        else:
            return False
    lecture_fixed.boolean = True

    def get_absolute_url(self):
        """
            Returns the url to access a particular classroom instance.
        """
        return reverse('course-detail', args=[str(self.id)])


class Day(models.Model):
    class Meta:
        db_table = 'Day'

    DAYS = (("monday", "Monday"), ("tuesday", "Tuesday"), ("wednesday", "Wednesday"),
            ("thursday", "Thursday"), ("friday", "Friday"), ("saturday", "Saturday"),
            ("sunday", "Sunday"))
    name = models.CharField(max_length=9, choices=DAYS, unique=True)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    class Meta:
        db_table = "TimeSlot"
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField()
    default_duration = timedelta(hours=1)
    duration = models.DurationField(default=default_duration, )
    day = models.ForeignKey(Day, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0} at {1} on {2} by {3}".format(self.course.title,
                                                self.classroom.name,
                                                self.day.name,
                                                self.start_time)


class FreeTime(models.Model):
    class Meta:
        db_table = "FreeTime"
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    available = ArrayField(models.PositiveSmallIntegerField())