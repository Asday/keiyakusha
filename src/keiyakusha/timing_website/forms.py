from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.functional import cached_property

from timing.models import TimeEntry


# TODO: Implement properly.
class AddTimeForm(forms.ModelForm):
    action = reverse_lazy('timing_website:add_time_form_view')

    class Meta:
        model = TimeEntry
        fields = (
            'start',
            'task',
            'note',
        )

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        self._user = user


class FinishCurrentTaskForm(forms.Form):
    action = reverse_lazy('timing_website:finish_current_task_form_view')

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        self._user = user

    def clean(self):
        if self.current_task is None:
            raise ValidationError(
                'You do not currently have a task running.',
                code='no_running_task',
            )

    def save(self):
        self.current_task.finish()

    @cached_property
    def current_task(self):
        return TimeEntry.objects.current_task(self._user)
