import os
import openai
from schema.alerta_schema import AlertaRequest
from typing import Dict
from fpdf import FPDF
import tempfile

# Configurar la API key de OpenAI
openai.api_key = "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"

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
    
    try:
        # Usar la nueva sintaxis de OpenAI (v1.0+)
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        parte_texto = response.choices[0].message.content.strip()
        
    except Exception as e:
        # Fallback en caso de error con la API
        parte_texto = f"Error al generar parte con IA: {str(e)}. Parte generado automáticamente basado en la alerta."
    
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
    """
    Genera un PDF del parte policial con formato oficial similar al ejemplo proporcionado.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Encabezado superior
    pdf.set_font("Arial", "", 10)
    pdf.cell(120, 8, f"Parte No.  {parte.get('pnc', '')}", border=0)
    pdf.cell(0, 8, f"Fecha y hora de impresión:  {parte.get('fecha', '')}    {parte.get('hora', '')}", border=0, ln=True, align="R")

    # Logo y título
    pdf.image("imagenes/Escudo_Policia.png", x=180, y=18, w=18)
    pdf.image("imagenes/Color=Black.png", x=160, y=20, w=18)
    pdf.set_xy(10, 20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, "REPÚBLICA DEL ECUADOR MINISTERIO DE GOBIERNO", ln=True, align="L")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, "NOTICIA DEL INCIDENTE", ln=True, align="L")
    pdf.ln(2)

    # Información de los aprehendidos/detenidos (simulada con nombre del policía)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Información de los aprehendidos/detenidos", ln=True, fill=True)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(10, 7, "No", border=1, align="C")
    pdf.cell(60, 7, "Nombre del Aprehendido", border=1, align="C")
    pdf.cell(40, 7, "Cédula", border=1, align="C")
    pdf.cell(40, 7, "Fecha Aprehensión", border=1, align="C")
    pdf.cell(30, 7, "Hora Aprehensión", border=1, ln=True, align="C")
    pdf.set_font("Arial", "", 9)
    pdf.cell(10, 7, "1", border=1, align="C")
    pdf.cell(60, 7, parte.get("nombre_policia", ""), border=1)
    pdf.cell(40, 7, parte.get("pnc", ""), border=1)
    pdf.cell(40, 7, parte.get("fecha", ""), border=1)
    pdf.cell(30, 7, parte.get("hora", ""), border=1, ln=True)
    pdf.ln(2)

    # Información general
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Información general", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(50, 6, f"Fecha Elaboración: {parte.get('fecha', '')}", ln=False)
    pdf.cell(60, 6, f"Parte Policial No.: {parte.get('pnc', '')}", ln=False)
    pdf.cell(0, 6, f"Rango: {parte.get('rango', '')}", ln=True)
    pdf.cell(50, 6, f"Unidad Policial: {parte.get('dispositivo', {}).get('tipo', '')}", ln=False)
    pdf.cell(60, 6, f"ID Dispositivo: {parte.get('dispositivo', {}).get('id', '')}", ln=False)
    pdf.cell(0, 6, f"IP: {parte.get('dispositivo', {}).get('ip', '')}", ln=True)
    pdf.ln(2)

    # Información de la unidad de policía
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Información de la unidad de policía que intervino en el hecho", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 6, f"{parte.get('descripcion', '')}")
    pdf.ln(1)

    # Información geográfica y cronológica del evento
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Información geográfica y cronológica del evento", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    coords = parte.get("coordenadas", {})
    pdf.cell(60, 6, f"Latitud: {coords.get('lat', '')}", ln=False)
    pdf.cell(60, 6, f"Longitud: {coords.get('lng', '')}", ln=False)
    pdf.cell(0, 6, f"Lugar: {parte.get('ubicacion', '')}", ln=True)
    pdf.cell(60, 6, f"Fecha del Hecho: {parte.get('fecha', '')}", ln=False)
    pdf.cell(60, 6, f"Hora aproximada: {parte.get('hora', '')}", ln=True)
    pdf.ln(2)

    # Clasificación del parte
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Clasificación del parte", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 6, "Tipo: JUDICIAL", ln=True)
    pdf.ln(1)

    # Información del hecho
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Información del hecho", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(60, 6, "Solicitado Por: ORDEN DE SERVICIO", ln=False)
    pdf.cell(60, 6, "Presunta flagrancia: NO", ln=False)
    pdf.cell(0, 6, "Tipo Operativo: ORDINARIO", ln=True)
    pdf.cell(0, 6, "Operativo: OPERATIVO ANTI DELINCUENCIALES", ln=True)
    pdf.ln(1)

    # Circunstancias del hecho
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Circunstancias del hecho", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    descripcion = parte.get("parte_ia", "")
    if descripcion:
        pdf.multi_cell(0, 6, descripcion.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(2)

    # Palabras clave y nivel de confianza
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 7, "Palabras clave:", ln=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 6, str(parte.get("palabras_clave", "")), ln=True)
    pdf.cell(0, 6, f"Nivel de confianza: {parte.get('nivel_confianza', '')}", ln=True)
    pdf.ln(5)

    # Pie de página
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, f"Página {pdf.page_no()} de 1", align="C")

    # Generar PDF en memoria
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            pdf.output(tmp.name)
        with open(tmp.name, 'rb') as f:
            pdf_bytes = f.read()
        os.unlink(tmp.name)
        return pdf_bytes
    except Exception as e:
        raise Exception(f"Error al generar PDF: {str(e)}")