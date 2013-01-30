import tornado.web
import plsql.core.catalog
from plsql.core.sqlcommand import SqlCommand

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db
	@property
	def catalog(self):
		return plsql.core.catalog.Catalog(self.db)

	@property
	def sql_command(self):
		return SqlCommand(self.db)

	def is_ajax(self):
		return "X-Requested-With" in self.request.headers and \
		self.request.handlers["X-Requested-With"]=="XMLHttpRequest"

