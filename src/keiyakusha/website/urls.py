from django.urls import include, path


urlpatterns = [
    path('timing/', include('timing_website.urls')),
]
