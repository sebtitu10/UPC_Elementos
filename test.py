from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# Usa tu URI real aquí o desde variable de entorno
uri = os.getenv("MONGO_URI", "mongodb+srv://<db_username>:<db_password>@cluster0.jjkrdho.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    print("🔌 Conectando a MongoDB...")
    client.admin.command('ping')
    print("✅ Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("❌ Error al conectar o hacer ping a MongoDB:")
    print(e)
finally:
    try:
        client.close()
        print("🔌 Conexión a MongoDB cerrada")
    except:
        pass