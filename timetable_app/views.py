from django.views.generic import TemplateView
from django.shortcuts import render
from .models import TimeSlot
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

