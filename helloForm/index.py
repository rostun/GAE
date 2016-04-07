import webapp2
import jinja2
import os

class BaseHandler(webapp2.RequestHandler):
	#cached_property means first time = calculate the value
	#after that, return value without calculating it (return stored value)
	@webapp2.cached_property
	def jinja2(self):
		return jinja2.Environment(
		#get a reference to the path that our template resides in
		loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True
		)

	#default to empty dictionary if do not supply template_variables
	def render(self, template, template_variables={}):
		template = self.jinja2.get_template(template)
		self.response.write(template.render(template_variables))