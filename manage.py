import os
from flask.ext.script import Manager, Shell, Server
from app import create_app
from app.scripts.disqus import DisqusCommand

app = create_app()

def _make_context():
    return dict(app=app)

manager = Manager(app)

manager.add_command("shell", Shell(make_context=_make_context))
manager.add_command("disqus",DisqusCommand)

if __name__ == "__main__":
    manager.run()