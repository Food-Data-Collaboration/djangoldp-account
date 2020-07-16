import sys

import django
from django.conf import settings
from djangoldp_account.tests import settings as settings_default

settings.configure(settings_default)

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_account.tests.tests_update',
])
if failures:
    sys.exit(failures)
