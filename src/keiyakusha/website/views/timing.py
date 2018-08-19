from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from timing.models import TimeEntry


class TimingView(LoginRequiredMixin, ListView):
    model = TimeEntry
    context_object_name = 'time_entries'

    def get_queryset(self):
        return self.model.objects.filter(engagement__user=self.request.user)

    def get_uninvoiced_data(self):
        return self.object_list \
            .uninvoiced() \
            .data()

    def get_this_week_data(self):
        return self.object_list \
            .from_this_week() \
            .data()

    def get_today_data(self):
        return self.object_list \
            .from_today() \
            .data()

    def get_current_task_data(self):
        current_task = TimeEntry.objects.current_task(self.request.user)

        return current_task and current_task.as_data()
