import webapp2
from google.appengine.ext import ndb
import db_models
import json

class Nation(webapp2.RequestHandler):
	def post(self):
		'''
		Creates a Nation Entity
		POST Body Variables:
		nname - Required. Country Name
		companies[] - Array of Company ids
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		new_nation = db_models.Nation()
		nname = self.request.get('nname', default_value=None)
		companies = self.request.get_all('companies[]', default_value=None)
		if nname: 
			new_nation.nname = nname
		else:
			self.response.status = 400
			self.response.status_message = "Invalid Request"
		if companies:
			for company in companies:
				new_nation.companies.append(ndb.Key(db_models.Company, int(company)))
		key = new_nation.put()
		out = new_nation.to_dict()
		self.response.write(json.dumps(out))
		return

#add company to a country
class NationCompanies(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		if 'nid' in kwargs:
			nation = ndb.Key(db_models.Nation, int (kwargs['nid'])).get()
			if not nation:
				self.response.status = 404
				self.response.status_message = "Nation not Found"
				return
		if 'cid' in kwargs:
			company = ndb.Key(db_models.Company, int(kwargs['cid']))
			if not company:
				self.response.status = 404
				self.response.status_message = "Company not Found"
				return
		if company not in nation.companies:
			nation.companies.append(company)
			nation.put()
		self.response.write(json.dumps(nation.to_dict()))
		return

#delete nation by id
class DeleteNation(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		if 'id' in kwargs:
			nationID = int(kwargs['id'])
			# nationID = int(self.request.get('key'))
			nation = db_models.Nation().get_by_id(int(nationID))
			nation.key.delete()
			self.response.status_message = "Country Deleted."
			return

#delete company from nation
class DeleteNationsCompany(webapp2.RequestHandler):
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type."
			return
		if 'nid' in kwargs:
			nation = ndb.Key(db_models.Nation, int (kwargs['nid'])).get()
			if not nation:
				self.response.status = 404
				self.response.status_message = "Nation not Found"
				return
		if 'cid' in kwargs:
			company = ndb.Key(db_models.Company, int(kwargs['cid']))
			if not company:
				self.response.status = 404
				self.response.status_message = "Company not Found"
				return
		nation.companies.remove(company)
		nation.put()
		return