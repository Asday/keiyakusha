from django.urls import path

from .views.timing import TimingView


urlpatterns = [
    path('timing/', TimingView.as_view())
]
