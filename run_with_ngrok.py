import subprocess
import time
import requests
import uvicorn
import threading
import os
from pathlib import Path

def run_fastapi():
    """Ejecutar la aplicación FastAPI"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

def run_ngrok():
    """Ejecutar ngrok para exponer el puerto 8000"""
    try:
        # Ejecutar ngrok
        subprocess.run(["ngrok", "http", "8000"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando ngrok: {e}")
    except FileNotFoundError:
        print("ngrok no encontrado. Asegúrate de que esté instalado y en el PATH")

def get_ngrok_url():
    """Obtener la URL pública de ngrok"""
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except:
        return None
    return None

if __name__ == "__main__":
    print("🚀 Iniciando Kuntur API con ngrok...")
    
    # Ejecutar FastAPI en un hilo separado
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Esperar un momento para que FastAPI se inicie
    print("⏳ Esperando que FastAPI se inicie...")
    time.sleep(3)
    
    # Ejecutar ngrok
    print("🌐 Iniciando ngrok...")
    ngrok_thread = threading.Thread(target=run_ngrok, daemon=True)
    ngrok_thread.start()
    
    # Esperar un momento para que ngrok se inicie
    time.sleep(2)
    
    # Obtener y mostrar la URL pública
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"✅ API expuesta públicamente en: {ngrok_url}")
        print(f"📊 Panel de ngrok: http://localhost:4040")
        print(f"🔗 Endpoints disponibles:")
        print(f"   - {ngrok_url}/docs (Documentación Swagger)")
        print(f"   - {ngrok_url}/api (API endpoints)")
        print(f"   - {ngrok_url}/webhook (Webhook endpoint)")
    else:
        print("⚠️  No se pudo obtener la URL de ngrok")
    
    print("\n🔄 Presiona Ctrl+C para detener...")
    
    try:
        # Mantener el script ejecutándose
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...") 