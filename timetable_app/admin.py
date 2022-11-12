from django.contrib import admin
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import HttpResponseRedirect
# from django.conf.urls import url
from django.urls import re_path as url
from django.utils.html import format_html
from .lecture import Lecture
from .models import Department, ClassRoom, Course, Day, TimeSlot, FreeTime

# Register your models here.
admin.site.register(Department)
admin.site.register(ClassRoom)
admin.site.register(Day)
admin.site.disable_action('delete_selected')

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
  list_display = (
    'course',
    'unit',
    'lecturer',
    'start_time',
    'length',
    'day',
    'classroom',
    'delete_lecture'
    )
  actions = ['delete_selected_lectures']

  def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
        url(
            r'^(?P<slot_id>.+)/delete/$',
            self.admin_site.admin_view(self.remove_selected_lecture),
            name='remove_selected_lecture',
        ),
    ]
    return custom_urls + urls

  def delete_lecture(self, obj):
    return format_html(
        '<a style="display: inline-block; height: 15px; background: #79aec8;\
        padding: 7px; border-radius: 3px;\
        margin-left: 10px; color: white" href="{}">Remove</a>',
        reverse('admin:remove_selected_lecture', args=[obj.pk]),
    )
  delete_lecture.short_description = 'Remove lecture'
  delete_lecture.allow_tags = True

  def remove_selected_lecture(self, request, slot_id, *args, **kwargs):
    lecture = self.get_object(request, slot_id)
    Lecture.remove_lecture(lecture)
    url = reverse(
        'admin:timetable_app_course_changelist',
    )
    self.message_user(request, "{0} has been removed from the timetable".format(lecture))
    return HttpResponseRedirect(url)

  def delete_selected_lectures(self, request, queryset):
    """
    Deletes all selected lectures from the timeslot
    """
    if len(queryset) > 0:
      for lecture in queryset:
        Lecture.remove_lecture(lecture)
        

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = (
        'code',
        'title',
        'department',
        'level',
        'lecture_fixed',
        'create_lecture'
    )
  actions = ['fix_selected_lectures', 'delete_selected_courses']

  def delete_selected_courses(self, request, queryset):
    if len(queryset) > 0:
      for course in queryset:
        self.remove_lecture(course)
      queryset.delete()

  def fix_selected_lectures(self, request, queryset):
    if len(queryset) > 0:
      for course in queryset:
        time_slots = TimeSlot.objects.filter(course=course)
        if time_slots:
          for slot in time_slots:
            Lecture.remove_lecture(slot)
      for course in queryset:
        lecture = Lecture(course)
        lecture.fix_lecture()

  def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
        url(
            r'^(?P<course_id>.+)/create/$',
            self.admin_site.admin_view(self.fix_lecture),
            name='fix-lecture',
        ),
    ]
    return custom_urls + urls
  
  def create_lecture(self, obj):
    return format_html(
        '<a style="display: inline-block; height: 15px; border-radius: 3px; background: #79aec8;\
        padding: 10px; margin-left: 7px; color: white" href="{}">Create</a>',
        reverse('admin:fix-lecture', args=[obj.pk]),
    )
  create_lecture.short_description = 'Create lecture'
  create_lecture.allow_tags = True

  def fix_lecture(self, request, course_id, *args, **kwargs):
    selected_course = self.get_object(request, course_id)
    time_slots = TimeSlot.objects.filter(course=selected_course)
    if time_slots:
      for slot in time_slots:
        Lecture.remove_lecture(slot)
    lecture = Lecture(selected_course)
    response = lecture.fix_lecture()
    url = reverse(
        'admin:timetable_app_course_changelist',
    )
    if response["status"] == "success":
      self.message_user(request, response["message"])
    else:
      self.message_user(request, response["message"])
    return HttpResponseRedirect(url)

  