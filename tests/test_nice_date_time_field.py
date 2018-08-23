import datetime

from django.utils import timezone

from freezegun import freeze_time
import pytest
import pytz

from timing_website.forms import NiceDateTimeField  # noqa


@freeze_time('2018-08-23 15:00:00.0', tick=True)
@pytest.mark.parametrize(
    'value,expected',
    [
        ('18/08/24 1500', (2018, 8, 24, 15)),
        ('18/08/22 1500', (2018, 8, 22, 15)),
        ('1600', (2018, 8, 22, 16)),
        ('1400', (2018, 8, 23, 14)),
    ],
)
def test_nice_date_time_field_input_parsing(value, expected):
    field = NiceDateTimeField()

    assert field.to_python(value) == datetime.datetime(
        *expected,
        tzinfo=pytz.UTC,
    )


@freeze_time('2018-08-23 15:00:00.0', tick=True)
def test_nice_date_time_takes_BST_into_account():
    timezone.activate('Europe/London')
    field = NiceDateTimeField()
    now = timezone.localtime(timezone.now())

    assert now.hour == 16  # Just checkin'.

    should_not_precess = field.to_python('1530')

    assert should_not_precess.hour == 15  # Again, just checkin'.
    assert should_not_precess.day == 23
    assert timezone.localtime(should_not_precess, timezone.utc).hour == 14

    should_precess = field.to_python('1630')

    assert should_precess.hour == 16
    assert should_precess.day == 22
    assert timezone.localtime(should_precess, timezone.utc).hour == 15
