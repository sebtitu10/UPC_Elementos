from database.database import get_mongo_collection

class AlertaRepository:
    def __init__(self):
        self.collection = get_mongo_collection("alertas2")

    def insertar_alerta(self, alerta_dict: dict):
        result = self.collection.insert_one(alerta_dict)
        return str(result.inserted_id) 