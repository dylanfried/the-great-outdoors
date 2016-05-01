from flask import current_app as app
from flask import Markup
from flask.ext.script import Command, Manager, Option
from disqusapi import DisqusAPI, Paginator
import time
import random
import csv
import traceback

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
        Option('--begins_with','-bw',dest="begins_with", default=None,
                help="To be used in conjunction with the `--posts` option to put a filtering criteria."),
        Option('--following_posts', '-fp', dest='following_posts', default=0,
                help="To be used in conjunction with the `--posts` option to follow the randomly chosen (+ optional filtering) posts with N subsequent posts from the same thread."),
        Option('--forums','-f',dest="forums",default=False,action="store_true",
                help="Print out a list of all forums we can find"),
    )

    def run(self,popular_posts=False,posts=False,history_limit=5000000,number_of_posts=25,trending_threads=False,begins_with=None,following_posts=0,forums=False):
        if following_posts > 0:
            raise NotImplementedError("`following_posts` not yet supported. Need to redo how we get random posts to first choose random thread.")
        disqus = DisqusAPI(app.config['DISQUS']['API_SECRET'], app.config['DISQUS']['API_KEY'])
        if posts:
            app.logger.debug("Retrieving random posts")
            for i in range(number_of_posts):
                results = disqus.posts.list(method="GET",limit=25,offset=random.randint(1,history_limit))
                if begins_with is not None:
                    found = False
                    for result in results:
                        if Markup(result.get('message',"")).striptags().lower().startswith(begins_with.lower()):
                            # Found one that starts with it
                            found = True
                            break
                    if not found:
                        app.logger.debug("Did not find matching post")
                        continue
                else:
                    result = results[0]
                print "FORUM:%s\nAUTHOR:%s\nDATE:%s\nPOST:%s\n" % (result.get('forum','N/A'),result.get('author',{}).get('name','ANONYMOUS'),result.get('createdAt','N/A'),result.get('message','N/A'))
        elif forums:
            app.logger.debug("Retrieving forums")
            paginator = Paginator(disqus.threads.list,method="GET",related="forum",limit=100)
            forums = []
            counter = 0
            try:
                for result in paginator:
                    counter += 1
                    if counter % 50 == 0:
                        print "COUNT: %s, # of forums: %s" % (counter, len(forums))
                    # Only add a forum to the list if it isn't already on the list
                    if result['forum']['id'] not in [f['ID'] for f in forums]:
                        forums.append({
                            "ID":result['forum']['id'].encode('utf-8'),
                            "URL":result['forum']['url'].encode('utf-8'),
                            "DESCRIPTION":(result['forum']['description'].encode('utf-8') if result['forum']['description'] else None),
                            "CATEGORY":(result['forum']['category'].encode('utf-8') if result['forum']['category'] else None)
                        })
            except:
                print "Breaking out and writing to file. Exc: %s" % traceback.format_exc()
            with open("forums.csv","w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['ID','URL','DESCRIPTION','CATEGORY'])
                writer.writeheader()
                writer.writerows(forums)
            # more = True
            # cursor = None
            # while more:
            #     results = disqus.forums.interestingForums(method="GET",cursor=cursor)
            #     for result in results:
            #         print result
            #     if results.cursor:
            #         more = results.cursor['more']
            #         cursor = results.cursor
            #     else:
            #         more = False
            # for result in p:
            #     print result
            #     #print "NAME: %s\tid: %s\tURL: %s\n" % (result['name'],result['id'],result['url'])
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

