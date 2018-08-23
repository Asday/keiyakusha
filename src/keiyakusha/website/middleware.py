from django.conf import settings
from django.utils import timezone

import pytz


def user_timezone_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            timezone_name = request.user.profile.timezone
        else:
            timezone_name = settings.TIME_ZONE

        timezone.activate(pytz.timezone(timezone_name))

        response = get_response(request)

        return response

    return middleware
