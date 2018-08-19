from django.urls import path

from .views import TimingView


urlpatterns = [
    path('', TimingView.as_view())
]
