import os
import sys


os.environ['DJANGO_SETTINGS_MODULE'] = 'projx.settings'

sys.path.append('/home/v21/')

import django.core.handlers.wsgi




application = django.core.handlers.wsgi.WSGIHandler()
