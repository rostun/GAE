from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		# two dictionary overrides
		d = super(Model, self).to_dict() # call original to_dict()
		d['key'] = self.key.id() # add key by pulling out its id
		return d

class Update(Model):
	date_time = ndb.DateTimeProperty(required=True)
	user_count = ndb.IntegerProperty(required=True)
	message_count = ndb.IntegerProperty(required=True)

class Nation(Model):
	nname = ndb.StringProperty(required=True)
	companies = ndb.KeyProperty(repeated=True)
	updates = ndb.StructuredProperty(Update, repeated=True)

	def to_dict(self):
		d = super(Nation, self).to_dict()
		d['companies' = [c.id() for c in d['companies']] # pulling out ids for each key
		return d

class Company(Model):
	cname = ndb.StringProperty(required=True)
	symbol = ndb.StringProperty(required=True)