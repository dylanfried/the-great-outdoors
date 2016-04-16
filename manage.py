import os
from flask.ext.script import Manager, Shell, Server
from app import create_app
from app.scripts.disqus import DisqusCommand

app = create_app()

def _make_context():
    return dict(app=app)

manager = Manager(app)

manager.add_command("shell", Shell(make_context=_make_context))
# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = False,
    host = '0.0.0.0',
    threaded=False)
)
manager.add_command("disqus",DisqusCommand)

if __name__ == "__main__":
    manager.run()