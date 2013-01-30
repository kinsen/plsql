import pymssql

from plsql.mssql.settings import mssql_settings

class MSSQLExecutor():
	def __get_connect(self):
		conn=pymssql.connect(
			host=mssql_settings["host"],
			user=mssql_settings["user"],
			password=mssql_settings["password"],
			database=mssql_settings["database"],
			as_dict=True)
		return conn
		

	def query(self,command_text,parameters):
		conn=self.__get_connect()
		cur=conn.cursor()
		if not cur:
			raise(NameError,"can't connect to mssql database!")

		sql_params=tuple([param[1] for param in parameters])
		cur.execute(command_text,sql_params)
		result=cur.fetchall()
		description=[desc[0] for desc in cur.description]
		conn.close()
		return result,description


