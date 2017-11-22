from django.contrib import admin
from .models import Department, ClassRoom, Course, Day, UserProfile

# Register your models here.
admin.site.register(Department)
admin.site.register(ClassRoom)
admin.site.register(Course)
admin.site.register(Day)
admin.site.register(UserProfile)
