from flask import Flask
from flask_script import Server, Manager, Command

from subsdash import create_app

manager = Manager(create_app('config.cfg'))

manager.add_command("runserver", Server('0.0.0.0',port=8090))

if __name__ == "__main__":
    manager.run()