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

sys.path[:] = ['/Users/euan/python/recipesplus',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/site-packages/setuptools-0.6c11-py2.5.egg',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/site-packages/pip-1.0.2-py2.5.egg',
 '/Users/euan/.virtualenvs/recipesplus/lib/python25.zip',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/plat-darwin',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/plat-mac',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/plat-mac/lib-scriptpackages',
 '/Users/euan/.virtualenvs/recipesplus/Extras/lib/python',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/lib-tk',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/lib-dynload',
 '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5',
 '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-darwin',
 '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/lib-tk',
 '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-mac',
 '/System/Library/Frameworks/Python.framework/Versions/2.5/lib/python2.5/plat-mac/lib-scriptpackages',
 '/Users/euan/.virtualenvs/recipesplus/lib/python2.5/site-packages']

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipesplus.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
