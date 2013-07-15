"""
WSGI config for recipesplus project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

sys.path[:] = [
 '/Users/euan/python/recipesplus',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/site-packages/pip-1.3.1-py2.7.egg',
 '/Users/euan/.virtualenvs/recipesplus/lib/python27.zip',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/plat-darwin',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/plat-mac',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/plat-mac/lib-scriptpackages',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/lib-tk',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/lib-old',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/lib-dynload',
 '/usr/local/lib/python2.7',
 '/usr/local/lib/python2.7/plat-darwin',
 '/usr/local/lib/python2.7/lib-tk',
 '/usr/local/lib/python2.7/plat-mac',
 '/usr/local/lib/python2.7/plat-mac/lib-scriptpackages',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.7/site-packages',
 ]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipesplus.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
