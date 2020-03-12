import unittest
import os

from flask_script import Server, Manager

from app import create_app, db


config_name = os.environ.get('APP_CONFIG')
app = create_app(config_name)

server = Server(host="0.0.0.0", port=8080)
manager = Manager(app)
manager.add_command("runserver", server)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
