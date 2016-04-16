from flask import current_app as app
from flask.ext.script import Command, Manager, Option
from disqusapi import DisqusAPI

class DisqusCommand(Command):

    option_list = (
    )

    def run(self):
        # Disqus's documentation on the official Python bindings are wrong. I modified to seemingly work
        # seems like you just chain on the resource and endpoint like so: `<API object>.resource.endpoint(args)`
        disqus = DisqusAPI(app.config['DISQUS']['API_SECRET'], app.config['DISQUS']['API_KEY'])
        for result in disqus.trends.listThreads(method='GET'):
            print result

