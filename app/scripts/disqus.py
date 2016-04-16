from flask import current_app as app
from flask.ext.script import Command, Manager, Option
from disqusapi import DisqusAPI
import time
import random

class DisqusCommand(Command):

    option_list = (
        Option("--popular_posts", "-pp", dest="popular_posts", default=False, action="store_true",
                help='Print out list of popular posts'),
        Option("--posts", "-p", dest="posts", default=False, action="store_true",
                help='Print out random list of posts'),
        Option("--history_limit","-hl", dest="history_limit",default=5000000,
                help="Upper bound of last N posts to search through."),
        Option("--number_of_posts", "-n", dest="number_of_posts", default=25,
                help="Number of posts to retrieve."),
        Option("--trending_threads", "-t", dest="trending_threads", default=False, action="store_true",
                help='Print out list of trending threads'),
    )

    def run(self,popular_posts=False,posts=False,history_limit=5000000,number_of_posts=25,trending_threads=False):
        disqus = DisqusAPI(app.config['DISQUS']['API_SECRET'], app.config['DISQUS']['API_KEY'])
        if posts:
            app.logger.debug("Retrieving random posts")
            for i in range(number_of_posts):
                results = disqus.posts.list(method="GET",limit=1,offset=random.randint(1,history_limit))
                result = results[0]
                print "FORUM:%s\nAUTHOR:%s\nDATE:%s\nPOST:%s\n" % (result.get('forum','N/A'),result.get('author',{}).get('name','ANONYMOUS'),result.get('createdAt','N/A'),result.get('message','N/A'))
        elif popular_posts:
            app.logger.debug("Retrieving popular posts")
            for result in disqus.posts.listPopular(method="GET",limit=number_of_posts):
                if result.get('message',None):
                    print "FORUM:%s\nAUTHOR:%s\nDATE:%s\nPOST:%s\n" % (result.get('forum','N/A'),result.get('author',{}).get('name','ANONYMOUS'),result.get('createdAt','N/A'),result.get('message','N/A'))
                    time.sleep(3)
        elif trending_threads:
            app.logger.debug("Retrieving trending threads")
            # Disqus's documentation on the official Python bindings are wrong. I modified to seemingly work
            # seems like you just chain on the resource and endpoint like so: `<API object>.resource.endpoint(args)`
            for result in disqus.trends.listThreads(method='GET'):
                print result

