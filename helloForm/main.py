import webapp2 #google's framework
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment( #create environment variable 
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates") #get a reference to the path that our template resides in 
)

class MainPage(webapp2.RequestHandler):
	template_variables = {}

	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.out.write(template.render())
	def post(self):
		self.template_variables['form_content'] = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		for i in self.request.arguments():
			self.template_variables['form_content'][i] = self.request.get(i)
		self.response.write(template.render(self.template_variables))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)