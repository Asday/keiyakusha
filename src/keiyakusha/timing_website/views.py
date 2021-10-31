from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from django_tables2 import RequestConfig

from timing.models import TimeEntry

from .forms import AddTimeForm, FinishCurrentTaskForm
from .tables import TimeEntryTable


class TimingView(LoginRequiredMixin, ListView):
    model = TimeEntry
    context_object_name = 'time_entries'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        table = TimeEntryTable(self.object_list)
        RequestConfig(self.request).configure(table)
        context['table'] = table

        add_time_form = self.get_add_time_form()
        context['add_time_form'] = add_time_form

        finish_current_task_form = self.get_finish_current_task_form()
        context['finish_current_task_form'] = finish_current_task_form

        return context

    def get_queryset(self):
        return (
            self.model.objects
            .filter(engagement__user=self.request.user)
            .order_by('-start')
            .with_end()
        )

    def get_add_time_form(self):
        kwargs = {'user': self.request.user}
        data = self.request.session.pop('add_time_form_data', None)

        if data is not None:
            kwargs['data'] = data

        return AddTimeForm(**kwargs)

    def get_finish_current_task_form(self):
        kwargs = {'user': self.request.user}
        data = self.request.session.pop('finish_current_task_form_data', None)

        if data is not None:
            kwargs['data'] = data

        return FinishCurrentTaskForm(**kwargs)

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


class SurrogateFormView(FormView):
    session_key = None
    blacklisted_fields = (
        'csrfmiddlewaretoken',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.http_method_names = [
            http_method_name for http_method_name in self.http_method_names
            if http_method_name != 'get'
        ]

    def form_valid(self, form):
        self.request.session.pop(self.session_key, None)

        return super().form_valid(form)

    def form_invalid(self, form):
        self.request.session[self.get_session_key()] = {
            field_name: field_data
            for field_name, field_data in form.data.items()
            if field_name not in self.blacklisted_fields
        }

        return HttpResponseRedirect(self.get_success_url())

    def get_session_key(self):
        if not self.session_key:
            raise ImproperlyConfigured('No session key provided.')

        return self.session_key


class AddTimeFormView(LoginRequiredMixin, SurrogateFormView):
    form_class = AddTimeForm
    success_url = reverse_lazy('timing_website:timing_view')
    session_key = 'add_time_form_data'

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user
        kwargs['data'] = self.request.POST.copy()

        return kwargs


class FinishCurrentTaskFormView(LoginRequiredMixin, SurrogateFormView):
    form_class = FinishCurrentTaskForm
    success_url = reverse_lazy('timing_website:timing_view')
    session_key = 'finish_current_task_form_data'

    def form_valid(self, form):
        form.save()

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs
