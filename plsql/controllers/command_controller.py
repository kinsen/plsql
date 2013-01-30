import tornado.web

from plsql.controllers.base import BaseHandler
from plsql.mssql.executor import MSSQLExecutor

class SqlCommandHandler(BaseHandler):
	def get(self,command_id):
		if command_id:
			command=self.sql_command.get_command(command_id)
			if command:
				return self.render("command_item.html",command=command)

		return self.render("command.html",commands=self.sql_command.get_all_command())
	
class SqlCommandCatalogHandler(BaseHandler):
	def get(self,catalog_id):
		if catalog_id:
			commands=self.sql_command.get_commands_by_catalog(catalog_id)
			return self.render("command.html",commands=commands)

		raise tornado.web.HTTPError(404)


class SqlCommandAddHandler(BaseHandler):
	def get(self):
		return self.render("command_add.html",catalogs=self.catalog.getAllCatalog())

	def post(self):
		catalogId=self.get_argument("catalogId")
		commandText=self.get_argument("commandText")
		parameters=self.get_argument("parameters")
		name=self.get_argument("name")
		description=self.get_argument("description")
		self.sql_command.add_command(catalogId,commandText,parameters,name,description)
		return self.redirect("/command")

class SqlCommandEditHandler(BaseHandler):
	def get(self,command_id):
		command=self.sql_command.get_command(command_id)
		if command:
			return self.render("command_edit.html",command=command,catalogs=self.catalog.getAllCatalog())
		raise tornado.web.HTTPError(404)

	def post(self,command_id):
		command=self.sql_command.get_command(command_id)
		if command:
			command.CatalogId=self.get_argument("catalogId")
			command.CommandText=self.get_argument("commandText")
			command.Parameters=self.get_argument("parameters","")
			command.Name=self.get_argument("name")
			command.Description=self.get_argument("description")
			self.sql_command.update_command(command)
			return self.redirect("/command")
		raise tornado.web.HTTPError(404)

class SqlCommandExcuteHandler(BaseHandler):
	def get(self,command_id):
		command=self.sql_command.get_command(command_id)
		if command:
			return self.render("command_execute.html",command=command)
		raise tornado.web.HTTPError(404)
	def post(self,command_id):
		command=self.sql_command.get_command(command_id)
		if not command:
			raise tornado.web.HTTPError(404)

		parameterList=[]
		for parameter in command.Parameters.split(','):
			parameterName=parameter.split(':')[0]
			parameterList.append((parameterName,self.get_argument(parameterName)))

		executor=MSSQLExecutor()
		result,description=executor.query(command.CommandText,parameterList)
		return self.render("command_report.html",result=result,description=description)

