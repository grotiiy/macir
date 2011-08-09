from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import iterableStringProperty
import iterableString
import os

class Point(db.Model):
    """Database object to store points"""

    id = iterableStringProperty.iterableStringProperty()
    point = db.GeoPtProperty()        
    

class MainPage(webapp.RequestHandler):
    def get(self):
        points = Point.all().order("-id")
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, locals()))

class Put(webapp.RequestHandler):
    def getLast(self):
        last = Point.all().order("-id").get()
        return last

    def putPoint(self,p):
        point = Point()
        point.point = p
        point.id = self.getLast().id.next()
        point.put()
        return point.id

    def get(self):
        la = self.request.get("la")
        lo = self.request.get("lo")
        point = db.GeoPt(la,lo)
        id = self.putPoint(point)
        self.response.out.write(id)


application = webapp.WSGIApplication([
        ('/', MainPage),
        ('/put',Put),
        
        ], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
