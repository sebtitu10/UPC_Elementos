# Configuración de ngrok para Kuntur API

## ¿Qué es ngrok?

ngrok es una herramienta que permite exponer tu servidor local a internet de forma segura, creando un túnel que hace que tu aplicación sea accesible desde cualquier lugar del mundo.

## Instalación

### 1. Instalar ngrok
```bash
# Windows (ya instalado)
winget install ngrok.ngrok

# O descargar manualmente desde https://ngrok.com/
```

### 2. Instalar dependencias de Python
```bash
pip install -r requirements.txt
```

## Configuración

### Opción 1: Uso automático (Recomendado)

Ejecuta el script que configura todo automáticamente:

```bash
python run_with_ngrok.py
```

Este script:
- Inicia tu aplicación FastAPI en el puerto 8000
- Inicia ngrok para exponer el puerto
- Muestra la URL pública generada
- Abre el panel de ngrok en http://localhost:4040

### Opción 2: Uso manual

1. **Inicia tu aplicación FastAPI:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. **En otra terminal, ejecuta ngrok:**
```bash
ngrok http 8000
```

## URLs disponibles

Una vez configurado, tendrás acceso a:

- **API Pública**: `https://[random-id].ngrok.io`
- **Documentación Swagger**: `https://[random-id].ngrok.io/docs`
- **Panel de ngrok**: `http://localhost:4040`

## Endpoints principales

- `POST /webhook` - Recibe eventos y notifica por WebSocket
- `GET /api/...` - Endpoints de la API
- `WS /ws/{client_id}` - Conexiones WebSocket

## Configuración avanzada

### Autenticación con ngrok (Opcional)

1. Regístrate en [ngrok.com](https://ngrok.com/)
2. Obtén tu authtoken
3. Configura ngrok:
```bash
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### Configuración personalizada

Edita el archivo `ngrok.yml` para personalizar la configuración:

```yaml
version: "2"
authtoken: YOUR_AUTH_TOKEN_HERE
tunnels:
  kuntur-api:
    addr: 8000
    proto: http
    subdomain: kuntur-api  # Solo disponible con cuenta paga
    inspect: true
```

## Solución de problemas

### Error: "ngrok no encontrado"
- Asegúrate de que ngrok esté instalado
- Reinicia tu terminal después de la instalación
- Verifica que ngrok esté en el PATH

### Error: "Puerto ya en uso"
- Verifica que no haya otra aplicación usando el puerto 8000
- Cambia el puerto en el script si es necesario

### Error de conexión
- Verifica que tu firewall no esté bloqueando ngrok
- Asegúrate de tener conexión a internet

## Seguridad

⚠️ **Importante**: 
- ngrok expone tu aplicación local a internet
- Solo usa para desarrollo y pruebas
- No uses en producción sin configuración de seguridad adicional
- Considera usar autenticación en ngrok para mayor seguridad

## Comandos útiles

```bash
# Ver estado de ngrok
curl http://localhost:4040/api/tunnels

# Ver logs de ngrok
ngrok http 8000 --log=stdout

# Configurar región específica
ngrok http 8000 --region=us
``` 