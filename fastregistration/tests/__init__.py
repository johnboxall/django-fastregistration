from registration_tests import *
from password_tests import *
from profile_tests import *
from login_logout_tests import *


# Disabled TEMPLATE_DIRS so that custom templates would not intefere with tests.
from django.conf import settings
settings.TEMPLATE_DIRS = ()
