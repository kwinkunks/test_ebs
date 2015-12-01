#!/usr/bin/env python
# -*- coding: utf 8 -*-
"""
Testing EBS and Webapp2 together.

:copyright: 2015 Agile Geoscience
"""
import os
import mimetypes

import webapp2
import jinja2

#############################
# Boilerplate template stuff
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def datetimeformat(value, format='%H:%M on %d.%m.%Y'):
    return value.strftime(format)

jinja_env.filters['datetimeformat'] = datetimeformat

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#############################
# Deal with static resources like CSS, JS, etc.
# I think EB might handle this on its own
class StaticHandler(Handler):
    def get(self, file):
        abs_path = os.path.abspath(os.path.join('static', file))
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'r')
            self.response.content_type = mimetypes.guess_type(abs_path)[0]
            self.response.out.write(f.read())
            f.close()
        except:
            self.response.set_status(404)

#############################
# This is where the handlers go
class TestHandler(Handler):
    def get(self):
        self.render('index.html')

class HelloWebapp2(Handler):
    def get(self):
        self.response.write('Hello, webapp2!')

#############################
# Paths
# n.b. app must be called 'application' for EB to run it
application = webapp2.WSGIApplication([
                           (r'/', HelloWebapp2),
                           (r'/test', TestHandler),
                           (r'/static/(.+)', StaticHandler),
                          ], debug=True)

#############################
# For running locally
def main():
    from paste import httpserver
    # httpserver.serve(app, host='127.0.0.1', port='8080')
    httpserver.serve(application)

if __name__ == '__main__':
    main()
