from database.database import get_mongo_collection

class ParteRepository:
    def __init__(self):
        self.collection = get_mongo_collection("parte2")

    def insertar_parte(self, parte_dict: dict):
        result = self.collection.insert_one(parte_dict)
        return str(result.inserted_id) 