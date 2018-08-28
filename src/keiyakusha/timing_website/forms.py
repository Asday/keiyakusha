import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.functional import cached_property

from clients.models import Client, Project, Task
from engagements.models import Engagement
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
    # TODO: Improve these `CharField`s.
    # They all take their `max_length` and `required` from the backing
    # model field's `max_length` and `blank` respectively.  It'd read
    # more nicely if they _directly_ referred to the model fields.
    # `ModelForm` already does this, so it's worth glancing at that to
    # see if there's a form field we could already be using instead, or
    # if we should just quickly roll our own.
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

    def clean_client(self):
        # Make sure we can get an engagement for the client.
        self.engagement_object

        return self.cleaned_data['client']

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
        return self.create_time_entry()

    def create_time_entry(self):
        project_name = self.cleaned_data['project']
        task_name = self.cleaned_data['task']
        note = self.cleaned_data.get('note', '')
        time_start = self.cleaned_data['start'].astimezone(timezone.utc)
        time_end = self.cleaned_data.get('end', None)

        duration = None
        if time_end is not None:
            time_end = time_end.astimezone(timezone.utc)

            duration = time_end - time_start

        with transaction.atomic():
            project, _created = Project.objects.get_or_create(
                client=self.client_object,
                name=project_name,
            )
            task, _created = Task.objects.get_or_create(
                project=project,
                external_reference=task_name,
            )

            time_entry = TimeEntry.objects.create(
                start=time_start,
                duration=duration,
                note=note,
                task=task,
                engagement=self.engagement_object,
            )

        return time_entry

    @cached_property
    def engagement_object(self):
        # TODO: Test.
        try:
            return Engagement.objects.current_for(
                user=self._user,
                client=self.client_object,
            )

        except Engagement.DoesNotExist as does_not_exist:
            raise ValidationError(
                'No active engagement found for %(client)s',
                code='engagement_not_found',
                params={'client': self.client_object},
            ) from does_not_exist

    @cached_property
    def client_object(self):
        # TODO: Test.
        client_name = self.cleaned_data['client']
        try:
            return Client.objects.get(name=client_name)

        except Client.DoesNotExist as does_not_exist:
            raise ValidationError(
                'Client %(name)s does not exist.',
                code='client_not_found',
                params={'name': client_name},
            ) from does_not_exist


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
