import webapp2 # google's framework

config = {'default-group': 'base-data'}

app = webapp2.WSGIApplication([ # basic routes, take us to the three classes
	('/', 'company.Company'),
	('/company', 'company.Company'), # company 
	('/addCompany', 'company.Company')
], debug=True, config=config)

# regular expressions
app.router.add(webapp2.Route(r'/company/<id:[0-9]+>', 'company.Company')) # will take a company and an id (string of integers), will look up an individual company
app.router.add(webapp2.Route(r'/company/search', 'company.CompanySearch')) # searches a thing
app.router.add(webapp2.Route(r'/company/deleteCompany/<id:[0-9]+>', 'company.DeleteCompany')) #delete a company
app.router.add(webapp2.Route(r'/nation/<id:[0-9]+>', 'nation.Nation')) # look up company
app.router.add(webapp2.Route(r'/nation/deleteNation/<id:[0-9]+>', 'nation.DeleteNation')) #delete a country
app.router.add(webapp2.Route(r'/nation/<nid:[0-9]+>/company/<cid:[0-9]+>', 'nation.NationCompanies')) # countries have a list of companies
app.router.add(webapp2.Route(r'/nation/<nid:[0-9]+>/deleteNationsCompany/<cid:[0-9]+>', 'nation.DeleteNationsCompany')) # delete a company from a nation