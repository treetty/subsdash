from flask import Flask, current_app
from flask_script import Server, Manager, Command, prompt_bool

from subsdash import create_app
from subsdash.extensions import db

manager = Manager(create_app('config.cfg'))

manager.add_command("runserver", Server('0.0.0.0', port=8090))


@manager.command
def createall():
    db.create_all()


@manager.command
def dropall():
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()

if __name__ == "__main__":
    manager.run()
