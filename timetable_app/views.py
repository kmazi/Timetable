from django.views.generic import TemplateView
from django.shortcuts import render
from .models import TimeSlot, Department
from .timetable import Timetable


class HomePage(TemplateView):
    template_name = "homepage.html"


class ShowTable(TemplateView):
    template_name = "timetable.html"

    def get_context_data(self, **kwargs):
        lecturer = self.request.user
        timetable = Timetable(timetable_for="lecturer", lecturer=lecturer).generate_timetable()
        context = super(ShowTable, self).get_context_data(**kwargs)
        context['timetable'] = timetable
        return context


class LevelTimetable(TemplateView):
    template_name = "timetable.html"

    def get_context_data(self, **kwargs):
        lecturer = self.request.user
        department = Department.objects.filter(id=int(self.kwargs['department_id']))
        level = int(self.kwargs['level'])
        timetable = Timetable(timetable_for="set", department=department).generate_timetable()
        context = super(LevelTimetable, self).get_context_data(**kwargs)
        context['departments'] = departments
        context['timetable'] = timetable
        return context
