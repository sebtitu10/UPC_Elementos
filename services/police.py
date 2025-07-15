import os
import openai
from schema.alerta_schema import AlertaRequest
from typing import Dict
from fpdf import FPDF
import tempfile

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

def generar_pdf_parte_policial(parte: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "República del Ecuador", ln=True, align="C")
    pdf.cell(0, 10, "Policía Nacional del Ecuador", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PARTE POLICIAL", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Fecha: {parte.get('fecha', '')}    Hora: {parte.get('hora', '')}", ln=True)
    pdf.cell(0, 10, f"Lugar: {parte.get('ubicacion', '')}", ln=True)
    coords = parte.get("coordenadas", {})
    pdf.cell(0, 10, f"Coordenadas: Lat {coords.get('lat', '')}, Lng {coords.get('lng', '')}", ln=True)
    pdf.cell(0, 10, f"Nombre del policía: {parte.get('nombre_policia', '')}", ln=True)
    pdf.cell(0, 10, f"Rango: {parte.get('rango', '')}", ln=True)
    pdf.cell(0, 10, f"PNC: {parte.get('pnc', '')}", ln=True)
    dispositivo = parte.get("dispositivo", {})
    pdf.cell(0, 10, f"Dispositivo: {dispositivo.get('tipo', '')} - ID: {dispositivo.get('id', '')} - IP: {dispositivo.get('ip', '')}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Descripción de los hechos:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, parte.get("parte_ia", ""))
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Palabras clave:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, parte.get("palabras_clave", ""), ln=True)
    pdf.cell(0, 10, f"Nivel de confianza: {parte.get('nivel_confianza', '')}", ln=True)
    pdf.ln(15)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "__________________________", ln=True, align="R")
    pdf.cell(0, 10, "Firma del policía actuante", ln=True, align="R")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        pdf.output(tmp.name)
        tmp.seek(0)
        pdf_bytes = tmp.read()
    return pdf_bytes
