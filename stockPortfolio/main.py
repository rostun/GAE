import webapp2 # google's framework

config = {'default-group': 'base-data'}

app = webapp2.WSGIApplication([ # basic route
	('/', 'company.Company'),
	('/company', 'company.Company'), # company 
], debug=True, config=config)

# regular expressions
app.router.add(webapp2.Route(r'/company/<id:[0-9]+>', 'company.Company')) # will take a company and an id (string of integers), will look up an individual company
app.router.add(webapp2.Route(r'/company/search', 'company.CompanySearch')) # searches a thing
app.router.add(webapp2.Route(r'/nation', 'nation.Nation'))
# how we add companies to countries
app.router.add(webapp2.Route(r'/nation/<nid:[0-9]+>/company/<cid:[0-9]+>', 'nation.NationCompanies')) # countries have a list of companie