import os.path
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import plsql.core.catalog

from plsql.controllers import home_controller,catalog_controller,command_controller
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="plsql database host")
define("mysql_database", default="PLSQL", help="plsql database name")
define("mysql_user", default="root", help="plsql database user")
define("mysql_password", default="123", help="plsql database pwd")

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[
			(r"/",home_controller.HomeHandler),
			(r"/catalog",catalog_controller.CatalogHandler),	
			(r"/catalog/add",catalog_controller.CatalogNewHandler),
			(r"/catalog/edit/(\d+)",catalog_controller.CatalogEditHandler),
			(r"/catalog/(\d+)/command",command_controller.SqlCommandCatalogHandler),
			(r"/command/*(\d*)",command_controller.SqlCommandHandler),
			(r"/command/add",command_controller.SqlCommandAddHandler),
			(r"/command/edit/(\d+)",command_controller.SqlCommandEditHandler),
			(r"/command/execute/(\d+)",command_controller.SqlCommandExcuteHandler),
		]
		settings=dict(
			title=u"PLSQL",
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			xsrf_cookies=True,
			cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

		self.db=tornado.database.Connection(
			host=options.mysql_host,
			database=options.mysql_database,
			user=options.mysql_user,
			password=options.mysql_password
		)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()