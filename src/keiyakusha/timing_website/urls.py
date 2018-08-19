from django.urls import path

from .views import AddTimeFormView, FinishCurrentTaskFormView, TimingView


app_name = 'timing_website'
urlpatterns = [
    path('', TimingView.as_view(), name='timing_view'),
    path(
        'finish-current-task/',
        FinishCurrentTaskFormView.as_view(),
        name='finish_current_task_form_view',
    ),
    path(
        'add-time/',
        AddTimeFormView,
        name='add_time_form_view',
    ),
]
