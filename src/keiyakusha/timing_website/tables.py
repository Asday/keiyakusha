from django_tables2 import Column, Table

from timing.models import TimeEntry
from website.columns import DurationColumn


class TimeEntryTable(Table):
    task = Column(order_by=(
        'task__project__client__name',
        'task__project__name',
        'task__external_reference',
    ))
    duration = DurationColumn()

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
