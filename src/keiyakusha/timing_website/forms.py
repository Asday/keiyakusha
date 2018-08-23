import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property

from timing.models import TimeEntry


class NiceDateTimeField(forms.fields.BaseTemporalField):
    input_formats = (
        '%y/%m/%d %H%M',
        '%y/%m/%d %H%M%S',
        '%y/%m/%d %H%M%S.%f',
        '%H%M',
        '%H%M%S',
        '%H%M%S.%f',
    )

    def strptime(self, value, format):
        parsed_datetime = timezone.make_aware(
            datetime.datetime.strptime(value, format),
        )

        # If we're parsing for a date, it's simple.
        if ' ' in format:
            return parsed_datetime

        # Otherwise we have to guess at the date.  Pick the closest
        # date in the past for the time.
        #
        # For example: if the current time is 1500, and the user inputs
        # 1600, the date should be guessed as yesterday.  If the user
        # inputs 1400, the date should be guessed as today.
        parsed_time = parsed_datetime.time()
        now = timezone.now()

        candidate = now.replace(
            hour=parsed_time.hour,
            minute=parsed_time.minute,
            second=parsed_time.second,
            microsecond=parsed_time.microsecond,
        )
        if candidate > now:
            candidate -= datetime.timedelta(days=1)

        return candidate


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
