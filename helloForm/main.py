import webapp2 #google's framework

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)