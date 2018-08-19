from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from timing.models import TimeEntry


# TODO: Should this subclass `ListView` instead?
class TimingView(LoginRequiredMixin, TemplateView):
    template_name = 'timing/index.html'

    def get_uninvoiced_data(self):
        return TimeEntry.objects \
            .filter(engagement__user=self.request.user) \
            .uninvoiced() \
            .data()

    def get_this_week_data(self):
        return TimeEntry.objects \
            .filter(engagement__user=self.request.user) \
            .from_this_week() \
            .data()

    def get_today_data(self):
        return TimeEntry.objects \
            .filter(engagement__user=self.request.user) \
            .from_today() \
            .data()

    def get_current_task_data(self):
        current_task = TimeEntry.objects.current_task(self.request.user)

        return current_task and current_task.as_data()
