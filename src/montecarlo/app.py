from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import django.utils.simplejson


class Result(db.Model):
    """Stores a results and provides handy properties."""

    estimated_pi = db.FloatProperty()
    num_iter = db.IntegerProperty()
    date = db.DateTimeProperty(auto_now=True)
    user = db.UserProperty()


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    def get(self):
        """Handles GET."""

        num_iter = int(self.request.GET.get('num_iter', 1000000))
        self.response.out.write(template.render('index.html', locals()))


class ResultHandler(webapp.RequestHandler):
    """Receives computed results and stores them."""

    def post(self):
        """Handles POST."""

        data = None
        try:
            data = django.utils.simplejson.loads(self.request.body)
        except ValueError, e:
            self.response.out.write('Server received malformed data (%s)' % e)
            return

        if data:
            resultset = Result(
                estimated_pi=data['estimated_pi'],
                num_iter=data['num_iter'],
                user=users.get_current_user()
            )
            resultset.put() 


class ChartHandler(webapp.RequestHandler):
    """Uses Google Visualization API to draw a chart from stored results.

    See documentation for 'Visualization: Scatter Chart' at:
    http://code.google.com/apis/charttools
    """

    def get(self):
        """Handles GET."""

        num = self.request.GET.get('num', 100)
        if num > 1000:
            num = 1000

        results = Result.all().order('-num_iter').order('-date').fetch(num)

        values = [r.estimated_pi for r in reversed(results)]

        num_rows = len(values)

        rows = []

        for i in range(num_rows):
            rows.append("%i, %i, %i" % (i, 0, i+1))
            rows.append("%i, %i, %f" % (i, 1, values[i]))

        if values:
            pi = sum(values)/num_rows
        else:
            pi = ''

        self.response.out.write(template.render('chart.html', locals()))


app = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/result', ResultHandler),
    ('/chart', ChartHandler),
], debug=True)


def main():
    """The main function."""

    webapp.util.run_wsgi_app(app)


if __name__ == '__main__':
    main()
