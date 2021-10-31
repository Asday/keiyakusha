from django import template


register = template.Library()


@register.filter(name='duration')
def duration(d):
    # Strip milliseconds.
    return str(d).split('.')[0]
