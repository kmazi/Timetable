from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf.urls import url
from django.utils.html import format_html
from .lecture import Lecture
from .models import Department, ClassRoom, Course, Day, TimeSlot, FreeTime

# Register your models here.
admin.site.register(Department)
admin.site.register(ClassRoom)
admin.site.register(Day)
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
  list_display = (
    'course',
    'start_time',
    'duration',
    'day',
    'classroom',
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = (
        'code',
        'title',
        'department',
        'level',
        'lecture_fixed',
        'create_lecture',
        'delete_lecture',
    )

  def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
        url(
            r'^(?P<course_id>.+)/create/$',
            self.admin_site.admin_view(self.fix_lecture),
            name='fix-lecture',
        ),
        url(
            r'^(?P<course_id>.+)/delete/$',
            self.admin_site.admin_view(self.remove_all_selected_lectures),
            name='remove_all_selected_lectures',
        ),
    ]
    return custom_urls + urls

  def delete_lecture(self, obj):
    return format_html(
        '<a style="display: inline-block; height: 15px; background: #79aec8;\
        padding: 10px; padding-buttom: 10px; margin-left: 10px; color: white" href="{}">Delete</a>',
        reverse('admin:remove_all_selected_lectures', args=[obj.pk]),
    )
  delete_lecture.short_description = 'Delete lecture'
  delete_lecture.allow_tags = True
  
  def create_lecture(self, obj):
    return format_html(
        '<a style="display: inline-block; height: 15px; background: #79aec8;\
        padding: 10px; padding-buttom: 10px; margin-left: 10px; color: white" href="{}">Create</a>',
        reverse('admin:fix-lecture', args=[obj.pk]),
    )
  create_lecture.short_description = 'Create lecture'
  create_lecture.allow_tags = True

  def remove_lecture(self, selected_course):
    time_slots = TimeSlot.objects.filter(course__code=selected_course.code, course__title=selected_course.title)
    if time_slots:
      for slot in time_slots:
        day = slot.day
        duration = slot.duration
        time = slot.start_time.hour
        start_time = [time] if duration.seconds//3600 == 1 else [time, time+1]
        free_time = FreeTime.objects.filter(lecturer=selected_course.lecturer, day=day).first()
        free_time.available.extend(start_time)
        free_time.save()
      time_slots.delete()
    
  def remove_all_selected_lectures(self, request, course_id, *args, **kwargs):
    selected_course = self.get_object(request, course_id)
    self.remove_lecture(selected_course)
    url = reverse(
        'admin:timetable_app_course_change',
        args=[selected_course.pk],
        current_app=self.admin_site.name,
    )
    self.message_user(request, 'Success')
    return HttpResponseRedirect(url)

  def fix_lecture(self, request, course_id, *args, **kwargs):
    selected_course = self.get_object(request, course_id)
    self.remove_lecture(selected_course)
    lecture = Lecture(selected_course)
    response = lecture.fix_lecture()
    url = reverse(
        'admin:timetable_app_course_change',
        args=[selected_course.pk],
        current_app=self.admin_site.name,
    )
    if response["status"] == "success":
      self.message_user(request, 'Success')
    else:
      self.message_user(request, 'Error')
    return HttpResponseRedirect(url)

  