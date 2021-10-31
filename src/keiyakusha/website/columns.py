from django_tables2 import Column

from .templatetags.website_tags import duration


class DurationColumn(Column):

    def render(self, value):
        return duration(value)
