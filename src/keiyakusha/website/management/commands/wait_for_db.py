import math
import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


def tanh_timeout(asymptote, max_tries):
    for i in range(max_tries):
        yield math.tanh(i / 5) * asymptote


class Command(BaseCommand):
    requires_system_checks = False

    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')

        for seconds in tanh_timeout(5, 5):
            try:
                self.check_migrations()
            except OperationalError:
                pass  # Not ready yet.
            else:  # nobreak
                return  # Database responded.

            time.sleep(seconds)

        raise TimeoutError('max tries exceeded')
