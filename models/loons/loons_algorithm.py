# -*- coding: utf-8 -*-
"""
Created on Tue Jan 03 13:30:41 2012

@author: tao hong
"""

import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os

class loonsAlgorithmPage(webapp.RequestHandler):
    def get(self):
        text_file1 = open('loons/loons_algorithm.txt','r')
        x = text_file1.read()         
        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01pop_uberheader.html', {'title'})
        html = html + template.render(templatepath + '02pop_uberintroblock_wmodellinks.html', {'model':'loons','page':'algorithm'})
        html = html + template.render(templatepath + '03pop_ubertext_links_left.html', {})                       
        html = html + template.render(templatepath + '04uberalgorithm_start.html', {
                'model':'loons', 
                'model_attributes':'Loons Population Model', 
                'text_paragraph':x})
        html = html + template.render(templatepath + '04ubertext_end.html', {})
        html = html + template.render(templatepath + '05pop_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06pop_uberfooter.html', {'links': ''})
        self.response.out.write(html)

app = webapp.WSGIApplication([('/.*', loonsAlgorithmPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
    
