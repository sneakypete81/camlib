#!/usr/bin/python
import os

virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import camlib
from camlib import app as application
camlib.setup(os.environ.get('OPENSHIFT_DATA_DIR', None))

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    url = 'localhost'
    port = 5000
    print 'Running on http://%s:%d' % (url, port)
    httpd = make_server(url, port, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()
