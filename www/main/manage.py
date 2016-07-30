#!/usr/bin/env python

from config import BasicConfig
import sys
sys.path.append(BasicConfig.BASE_DIR)

from flask_script import Manager
from main import create_app
import os


manager = Manager()

conf_name = os.environ.get("FLAKS_CONFIG", "default")

app = create_app(conf_name)
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
