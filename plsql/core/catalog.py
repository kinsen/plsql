
class Catalog():
	def __init__(self,db):
		self.db=db

	def getAllCatalog(self):
		return self.db.query("SELECT * FROM Catalog")

	def getCatalog(self,catalogId):
		return self.db.get("SELECT * FROM Catalog where catalogId=%s",catalogId)

	def addCatalog(self,name,description):
		catalog=self.db.get("SELECT * FROM Catalog WHERE Name = %s",name)
		if not catalog:
			self.db.execute("INSERT INTO Catalog (Name,Description,CreateTime) VALUES(%s,%s,now())",name,description)

	def updateCatalog(self,model):
		if model:
			self.db.execute(
				"UPDATE Catalog SET Name=%s,Description=%s"
				"WHERE catalogId=%s",model.Name,model.Description,model.CatalogId
				)
