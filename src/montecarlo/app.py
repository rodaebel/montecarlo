# -*- coding: utf-8 -*-
#
# Copyright 2010 Tobias Rodäbel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sample GAE app for distributing Monte Carlo Simulations to compute Pi."""

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import deferred
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from models import Record, deferred_put

import json


def get_login_or_logout(user):
    """Returns login/logout link."""

    link = '<a href="%(href)s">%(label)s</a>'

    if user:
        return link % dict(href=users.create_logout_url('/'), label='Logout')

    return link % dict(href=users.create_login_url('/'), label='Login')


class MainHandler(webapp.RequestHandler):
    """The main handler."""

    def get(self):
        """Handles GET."""

        login_or_logout = get_login_or_logout(users.get_current_user())
        num_iter = int(self.request.GET.get('num_iter', 1000000))
        self.response.out.write(template.render('index.html', locals()))


class RecordHandler(webapp.RequestHandler):
    """Receives computed results and stores them."""

    def post(self):
        """Handles POST."""

        if not users.get_current_user():
            self.response.out.write('Only logged in users can record data.')
            return

        data = None
        try:
            data = json.loads(self.request.body)
        except ValueError, e:
            self.response.out.write('Server received malformed data (%s)' % e)
            return

        if data:
            record = Record(
                estimated_pi=float(data['estimated_pi']),
                num_iter=data['num_iter'],
                duration_ms=data['duration_ms'],
                user=users.get_current_user()
            )
            deferred.defer(
                deferred_put, [db.model_to_protobuf(record).Encode()])


class ChartHandler(webapp.RequestHandler):
    """Uses Google Visualization API to draw a chart from stored records.

    See documentation for 'Visualization: Scatter Chart' at:
    http://code.google.com/apis/charttools
    """

    def get(self):
        """Handles GET."""

        height = self.request.GET.get('height', 600)
        width = self.request.GET.get('width', 1000)
        num = int(self.request.GET.get('num', 100))
        if num > 1000:
            num = 1000

        records = Record.all().order('-num_iter').order('-date').fetch(num)

        values = [r.estimated_pi for r in records]

        num_rows = len(values)

        rows = []

        for i in range(num_rows):
            rows.append("%i, 0, %i" % (i, i+1))
            rows.append("%i, 1, %f" % (i, values[i]))

        if values:
            pi = sum(values)/num_rows
        else:
            pi = 'unknown'

        self.response.out.write(template.render('chart.html', locals()))


application = webapp.WSGIApplication([
    ('/', MainHandler),
    ('/record', RecordHandler),
    ('/chart', ChartHandler),
], debug=True)
