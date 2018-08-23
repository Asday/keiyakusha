import datetime

from freezegun import freeze_time
import pytest
from pytz import UTC

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

    assert field.to_python(value) == datetime.datetime(*expected, tzinfo=UTC)
