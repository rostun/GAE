import webapp2 #google's framework

config = {'default-group':'base-data'}

app = webapp2.WSGIApplication([
	('/edit/channel', 'edit_channel.EditChannel'),
	('/edit', 'edit.Edit'),
	('/channel/add', 'add_channel.AddChannel'),
	('/', 'admin.Admin'),
	#('/index', 'index.MainPage'),
], debug=True, config=config)