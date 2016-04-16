from flask import current_app as app
from flask.ext.script import Command, Manager, Option
from disqusapi import DisqusAPI
import time

class DisqusCommand(Command):

    option_list = (
        Option("--popular_posts", "-pp", dest="popular_posts", default=False, action="store_true",
                help='Print out list of popular posts'),
        Option("--trending_threads", "-t", dest="trending_threads", default=False, action="store_true",
                help='Print out list of trending threads'),
    )

    def run(self,popular_posts=False,trending_threads=False):
        disqus = DisqusAPI(app.config['DISQUS']['API_SECRET'], app.config['DISQUS']['API_KEY'])
        if popular_posts:
            app.logger.debug("Executing popular posts")
            for result in disqus.posts.listPopular(method="GET"):
                if result.get('message',None):
                    print "AUTHOR:%s\nDATE:%s\nPOST:%s\n" % (result.get('author',{}).get('name','ANONYMOUS'),result.get('createdAt','N/A'),result.get('message','N/A'))
                    time.sleep(3)
        elif trending_threads:
            app.logger.debug("Executing trending threads")
            # Disqus's documentation on the official Python bindings are wrong. I modified to seemingly work
            # seems like you just chain on the resource and endpoint like so: `<API object>.resource.endpoint(args)`
            for result in disqus.trends.listThreads(method='GET'):
                print result

