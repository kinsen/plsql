
class SqlCommand():
	def __init__(self,db):
		self.db=db

	def get_all_command(self):
		return self.db.query("SELECT s.*,c.Name as CatalogName FROM SQLCommand s "
			"JOIN Catalog c ON c.CatalogId=s.CatalogId ")

	def get_command(self,command_id):
		return self.db.get("SELECT s.*,c.Name as CatalogName FROM SQLCommand s "
			"JOIN Catalog c ON c.CatalogId=s.CatalogId "
			"WHERE CommandId=%s",int(command_id))

	def get_commands_by_catalog(self,catalog_id):
		return self.db.query("SELECT s.*,c.Name as CatalogName FROM SQLCommand s "
			"JOIN Catalog c ON c.CatalogId=s.CatalogId "
			"WHERE s.CatalogId=%s",int(catalog_id))


	def add_command(self,catalog_id,command_text,parameters,name,description):
		self.db.execute("""INSERT INTO SQLCommand(CatalogId,CommandText,Parameters,Name,Description,CreateTime) 
			VALUES (%s,%s,%s,%s,%s,now())
			""",int(catalog_id),command_text,parameters,name,description)

	def update_command(self,command):
		if command:
			self.db.execute("UPDATE SQLCommand SET CatalogId=%s,CommandText=%s"
				",Parameters=%s,Name=%s,Description=%s WHERE CommandId=%s",
				command.CatalogId,command.CommandText,
				command.Parameters,command.Name,command.Description,command.CommandId)
