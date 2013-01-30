import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from plsql.controllers.base import BaseHandler

class CatalogHandler(BaseHandler):
	def get(self):
		self.render("catalog.html",catalogs=self.catalog.getAllCatalog())

class CatalogNewHandler(BaseHandler):
	def get(self):
		self.render("catalog_new.html")

	def post(self):
		name=self.get_argument("name")
		description=self.get_argument("description")
		self.catalog.addCatalog(name,description)
		self.redirect("/catalog")

class CatalogEditHandler(BaseHandler):
	def get(self,catalogId):
		catalog=self.catalog
		model=catalog.getCatalog(catalogId)
		if model:
			return self.render("catalog_edit.html",catalog=model)
		raise tornado.web.HTTPError(404)

	def post(self,catalogId):
		catalog=self.catalog
		model=catalog.getCatalog(catalogId)
		if model:
			model.Name=self.get_argument("name")
			model.Description=self.get_argument("description")
			catalog.updateCatalog(model)
			return self.redirect("/catalog")
		raise tornado.web.HTTPError(404)
