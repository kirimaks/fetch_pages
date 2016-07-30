#!/usr/bin/env python

from main.config import BasicConfig
import sys
sys.path.append(BasicConfig.BASE_DIR)

from flask_script import Manager
from main import create_app
from main import cmd
import os


conf_name = os.environ.get("FLAKS_CONFIG", "default")

app = create_app(conf_name)
manager = Manager(app)
manager.add_command("uwsgi", cmd.CmdUwsgi())

if __name__ == "__main__":
    manager.run()
