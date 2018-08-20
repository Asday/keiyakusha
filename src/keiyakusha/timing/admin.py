from django.contrib.admin import ModelAdmin, site

from .models import TimeEntry


class TimeEntryAdmin(ModelAdmin):
    save_as = True


site.register(TimeEntry, TimeEntryAdmin)
