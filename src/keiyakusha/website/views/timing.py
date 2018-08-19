from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django_tables2 import Column, RequestConfig, Table

from timing.models import TimeEntry


class TimeEntryTable(Table):
    task = Column(order_by=(
        'task__project__client__name',
        'task__project__name',
        'task__external_reference',
    ))

    class Meta:
        # TODO: May be better to have this in settings?
        template_name = 'django_tables2/bootstrap4.html'
        model = TimeEntry
        fields = (
            'start_date',
            'start_time',
            'end_time',
            'duration',
            'task',
        )

    def _order_by_date(self, qs, is_descending):
        return (qs.order_by(f'{"-" if is_descending else ""}start'), True)

    def order_start_date(self, qs, is_descending):
        return self._order_by_date(qs, is_descending)

    def order_start_time(self, qs, is_descending):
        return self._order_by_date(qs, is_descending)

    def order_end_time(self, qs, is_descending):
        return self._order_by_date(qs, is_descending)


class TimingView(LoginRequiredMixin, ListView):
    model = TimeEntry
    context_object_name = 'time_entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        table = TimeEntryTable(self.object_list.order_by('-start'))
        RequestConfig(self.request).configure(table)
        context['table'] = table

        return context

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
