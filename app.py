# -*- coding: utf-8 -*-
__author__ = 'xiejdm'

from App import app

# from flask_script import Manager, Server


app = app
# manager = Manager(app)
# manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
