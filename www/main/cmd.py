import os
from flask_script import Command


class CmdUwsgi(Command):
    def run(self):
        print("Run uwsgi!")
        os.system("uwsgi --ini conf/uwsgi.ini")
