# Chat en tiempo real - Python Socket

Sistema de chat simple y eficiente usando sockets TCP en Python.

## Requisitos

- Python 3.6 o superior
- Bibliotecas estándar (socket, threading, json)

## Instalación

1. Descarga los archivos:
   - `servidor.py`
   - `cliente.py`

2. No requiere instalación de dependencias adicionales

## Cómo Ejecutar?

### Paso 1: Iniciar el Servidor

Abre una terminal y ejecuta:
```bash
python3 servidor.py
```

Verás el mensaje:
```
Servidor iniciado en localhost:5555
```

### Paso 2: Conectar Clientes

Abre **nuevas terminales** (una por cada usuario) y ejecuta:
```bash
python3 cliente.py
```

Cuando te pida el Usuario, escribe tu nombre y presiona Enter.


## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `/help` | Muestra todos los comandos |
| `/users` | Lista usuarios conectados |
| `/whisper <usuario> <mensaje>` | Envía mensaje privado |
| `/quit` | Desconecta del chat |

## Un ejemplo de Uso
```
USUARIO: Juan
Bienvenido Juan!
Escribe /help para comandos

Historial:
[14:30] María: Hola a todos
[14:32] Pedro: Qué tal?

Hola! ¿Cómo están?
[14:35] Juan: Hola! ¿Cómo están?

/whisper María Hola María, ¿cómo estás?
Mensaje enviado a María

/users
Usuarios conectados (3):
  Juan
  María
  Pedro

/quit
Hasta pronto!
Desconectado del servidor
```

## Características

- ✅ Chat en tiempo real
- ✅ Mensajes privados
- ✅ Historial de mensajes (últimos 50)
- ✅ Múltiples usuarios simultáneos
- ✅ Usernames únicos
- ✅ Persistencia de historial en JSON

## Archivos Generados

- `chat_history.json` - Historial de mensajes (se crea automáticamente)

## Notas

- El servidor debe estar ejecutándose antes de conectar clientes
- Los usernames deben ser únicos
- El historial se guarda automáticamente
- Usa `Ctrl+C` para cerrar el servidor de forma segura

## Solución de Problemas

**Error: "Address already in use"**
- Espera unos segundos o cambia el puerto en ambos archivos

**No puedo conectarme**
- Verifica que el servidor esté ejecutándose
- Confirma la IP y puerto correctos
- Revisa el firewall

**El cliente no responde**
- Verifica tu conexión de red
- Reinicia el cliente
