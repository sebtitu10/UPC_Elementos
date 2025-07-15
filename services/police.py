import os
import openai
from schema.alerta_schema import AlertaRequest
from typing import Dict

def generar_parte_policial(alerta: AlertaRequest) -> Dict:
    """
    Recibe una alerta, la procesa con un modelo IA (OpenAI GPT) y devuelve un parte policial formateado.
    """
    prompt = f"""
    Eres un asistente policial. Dado el siguiente reporte de alerta, genera un parte policial claro, formal y detallado:
    
    Alerta: {alerta.alerta or 'Sin título'}
    Descripción: {alerta.descripcion}
    Ubicación: {alerta.ubicacion}
    Coordenadas: lat {alerta.coordenadas.lat}, lng {alerta.coordenadas.lng}
    Fecha: {alerta.fecha}
    Hora: {alerta.hora}
    Nivel de confianza: {alerta.nivelConfianza}
    Nombre del policía: {alerta.nombrePolicia}
    Palabras clave: {alerta.palabrasClave}
    PNC: {alerta.pnc}
    Rango: {alerta.rango}
    Dispositivo: {alerta.dispositivo.dict()}
    
    Redacta el parte policial de la mejor manera posible:
    """
    openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...pon-tu-clave...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    parte_texto = response.choices[0].message.content.strip()
    parte_policial = {
        "titulo": f"Parte policial generado para alerta: {alerta.alerta or 'Sin título'}",
        "descripcion": alerta.descripcion,
        "ubicacion": alerta.ubicacion,
        "coordenadas": {
            "lat": alerta.coordenadas.lat,
            "lng": alerta.coordenadas.lng
        },
        "fecha": alerta.fecha,
        "hora": alerta.hora,
        "nivel_confianza": alerta.nivelConfianza,
        "nombre_policia": alerta.nombrePolicia,
        "palabras_clave": alerta.palabrasClave,
        "pnc": alerta.pnc,
        "rango": alerta.rango,
        "dispositivo": alerta.dispositivo.dict(),
        "parte_ia": parte_texto
    }
    return parte_policial
