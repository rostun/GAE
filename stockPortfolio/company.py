import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Company(webapp2.RequestHandler):
	def post(self):
		'''
		Creates a Company entity
		name - Required
		symbol - Required
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		new_company = db_models.Company()
		cname = self.request.get('cname', default_value=None)
		symbol = self.request.get('symbol', default_value=None)
		if cname:
			new_company.cname = cname
		else:
			self.response.status = 400
			self.response.status_message = "Invalid Request, Company name is Required."
		if symbol:
			new_company.symbol = symbol
		else:
			self.response.status = 400
			self.response.status_message = "Invalid Request, Company Symbol is Required."
		key = new_company.put() # save in database
		out = new_company.to_dict() # return the thing we just made
		self.response.write(json.dumps(out))
		return
	def get(self, **kwargs): #keyword arguments, in this case 'id'
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		# looking for id in keyword arguments 
		if 'id' in kwargs: # if it's there we make a key for a Country by passing in a type of company and id 
			out = ndb.Key(db_models.Company, int(kwargs['id'])).get().to_dict()     # from key we get the Country and turn it into a dictionary (python datatype)
			self.response.write(json.dumps(out)) # dump that to a json string and write it back as a response
		else: # if no id passed in keyword argumetns then we return all the key ids
			q = db_models.Company.query()
			keys = q.fetch(keys_only=True)
			results = {'keys': [x.id() for x in keys]}
			self.response.write(json.dumps(results))

# can search by a company name or symbol
class CompanySearch(webapp2.RequestHandler):
	def post(self):
		'''
		Search for Companies
		POST Body Variables:
		cname - String. Company name
		symbol - String. Company Symbol
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		q = db_models.Company.query()
		# applying some filters, passing in those keys, getting information
		if self.request.get('cname',None):
			q = q.filter(db_models.Company.cname == self.request.get('cname'))
		if self.request.get('symbol', None):
			q = q.filter(db_models.Company.symbol == self.request.get('symbol'))
		keys = q.fetch(keys_only=True)
		results = {'keys' : [x.id() for x in keys]}
		self.response.write(json.dumps(results))

#delete company by id
class DeleteCompany(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		if 'id' in kwargs:
			companyID = int(kwargs['id'])
			company = db_models.Company().get_by_id(int(companyID))

			nations = db_models.Nation.query()
			# nation = nation.filter(db_models.Nation.companies == ndb.Key(db_models.Company, companyID))
			for nation in nations:
				self.response.write(" FOR LOOP ")
				for id in nation.companies:
					self.response.write(" ANOTHER FOR LOOP ")
					if company.key == id:
						self.response.write(" FOUND COMPANY ")
						nation.companies.remove(id)
						nation.put()
					self.response.write(company.key)
					self.response.write(id)
				self.response.write(json.dumps(nation.to_dict()))

			company.key.delete()
			self.response.write("company deleted")