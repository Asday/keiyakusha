import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property

from clients.models import Client, Project, Task
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
    unambiguous_formats = {
        'microsecond': input_formats[2],
        'second': input_formats[1],
        'minute': input_formats[0],
    }

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
        now = timezone.localtime(timezone.now())

        candidate = now.replace(
            hour=parsed_datetime.hour,
            minute=parsed_datetime.minute,
            second=parsed_datetime.second,
            microsecond=parsed_datetime.microsecond,
        )

        if candidate > now:
            candidate = candidate.astimezone(timezone.utc)
            candidate = candidate.replace(day=candidate.day - 1)
            candidate = candidate.astimezone(timezone.get_current_timezone())

        return candidate

    def to_python(self, value):
        if value in self.empty_values:
            return None

        if isinstance(value, datetime.datetime):
            return value

        return super().to_python(value)

    @classmethod
    def strftime(cls, value):
        # TODO: Test.
        if not isinstance(value, datetime.datetime):
            raise ValueError('`value` must be a `datetime.datetime`')

        for name, format_ in cls.unambiguous_formats.items():
            # Haha dictionaries are ordered now!  :D
            if getattr(value, name):
                # If the value isn't zero, render at that resolution.
                return value.strftime(format_)

        # If even the minutes are zero, doesn't matter, we're gonna
        # render them anyway.  The lowest resolution we'll render is
        # `YY/MM/DD HHMM`.
        return value.strftime(cls.unambiguous_formats['minute'])


# This is going to be the big bad boy form for basically the entire
# time tracking portion of this project.
class AddTimeForm(forms.Form):
    action = reverse_lazy('timing_website:add_time_form_view')

    start = NiceDateTimeField()
    end = NiceDateTimeField(required=False)
    task = forms.CharField(
        max_length=Task._meta.get_field('external_reference').max_length,
    )
    note = forms.CharField(
        max_length=TimeEntry._meta.get_field('note').max_length,
        required=False,
    )
    project = forms.CharField(
        max_length=Project._meta.get_field('name').max_length,
    )
    client = forms.CharField(
        max_length=Client._meta.get_field('name').max_length,
    )

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)

        self._user = user

    def clean(self):
        super().clean()

        start = self.cleaned_data['start']
        end = self.cleaned_data.get('end', None)

        if end is not None and start >= end:
            self.add_error(
                'start',
                ValidationError(
                    'Start time cannot be after end time.',
                    code='start_after_end',
                ),
            )

            # Render the time fields less ambiguously, (with the date),
            # so the user sees where the issue has crept in.
            self.data['start'] = self.fields['start'].strftime(start)
            self.data['end'] = self.fields['end'].strftime(end)

    def save(self):
        # TODO: Implement.
        print(self.cleaned_data)


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
