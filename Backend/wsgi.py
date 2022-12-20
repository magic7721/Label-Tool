import sys
import os
import coverage
from app import create_app

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

COV = coverage.coverage(branch=True, include='app/*')
COV.start()

app = create_app("dev")

# http_server = HTTPServer(WSGIContainer(app))
# http_server.listen(5000)
# IOLoop.instance().start()


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    exit_code = unittest.TextTestRunner().run(tests).wasSuccessful()
    COV.stop()
    COV.save()
    COV.report()
    sys.exit(0 if exit_code else 1)
