from flask_script import Command
import subprocess


class CmdUwsgi(Command):
    def run(self):
        cmd = ['uwsgi', '--ini', 'conf/uwsgi.ini']
        subprocess.Popen(cmd)
