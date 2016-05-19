#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#

# -*- coding: utf-8 -*- 
import webapp2
from google.appengine.ext import ndb
import cgi
import urllib

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)
#Read Data
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)

        for greeting in greetings:
            self.response.out.write('<blockquote>%s</blockquote>' %
                                    cgi.escape(greeting.content))
#Insert Data
class Create(webapp2.RequestHandler):
    def post(self):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        guestbook_name = self.request.get('guestbook_name')
        test = urllib.unquote(guestbook_name.encode('ascii')).decode('utf-8')
        print '<p>%s</p>'%test
        content=self.request.get('content')
        con = urllib.unquote(content.encode('ascii')).decode('utf-8')
        print '<p>%s</p>'%con
        #try:
        #    greeting = Greeting(parent=ndb.Key("Book",test ),con)
        #    greeting.put()
        #    self.redirect('/')
        #except e :
        #    print '<p>%s</p><p>%s</p>'%(test,con)

#Update data
class Update(webapp2.RequestHandler):
    def post(self):
        self.response.write('Update')
#Delete data
class Delete(webapp2.RequestHandler):
    def post(self):
        self.response.write('Delete')

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/insert',Create),('/update',Update),('/delete',Delete)
], debug=True)
