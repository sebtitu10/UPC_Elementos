from services.police import generar_parte_policial, generar_pdf_parte_policial
from schema.alerta_schema import AlertaRequest, Coordenadas, Dispositivo

# Crea un objeto de prueba (ajusta los campos según tu modelo)
alerta = AlertaRequest(
    alerta="Robo en la vía pública",
    descripcion="Se reporta un robo en la Av. Principal...",
    ubicacion="Av. Principal y Calle Secundaria",
    coordenadas=Coordenadas(lat=-2.208327266181756, lng=-79.94152307510377),
    fecha="10/05/2022",
    hora="13:30",
    nivelConfianza="ALTA",
    nombrePolicia="ARISTEGA VERA FABIAN JONATHAN",
    palabrasClave="robo, flagrancia, patrullaje",
    pnc="0923438865",
    rango="SGO",
    dispositivo=Dispositivo(tipo="RADIO", id="12345", ip="192.168.1.1")
)

parte = generar_parte_policial(alerta)
pdf_bytes = generar_pdf_parte_policial(parte)

# Guarda el PDF en disco para revisarlo
with open("parte_policial_prueba.pdf", "wb") as f:
    f.write(pdf_bytes)

print("PDF generado: parte_policial_prueba.pdf")
