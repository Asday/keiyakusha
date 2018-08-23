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
    unambiguous_formats = {
        'microsecond': input_formats[2],
        'second': input_formats[1],
        'minute': input_formats[0],
    }

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
