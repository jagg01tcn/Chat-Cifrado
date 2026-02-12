# Chat-Cifrado

Cliente y servidor de chat multiusuario  TLS en Python orientados a  comunicaciones cifradas.  
Diseñado para despliegue en entornos controlados y VPS con análisis de TLS, concurrencia y diseño cliente–servidor.

---

## 1. Propósito del repositorio
Este repositorio implementa un **sistema de chat cifrado mediante TLS** compuesto por un cliente con interfaz gráfica y un servidor multi‑cliente concurrente.

El objetivo principal es servir como **entorno práctico de análisis de seguridad**, permitiendo evaluar:
- Configuración TLS básica y sus limitaciones.
- Comunicación cliente–servidor cifrada.
- Gestión concurrente de sesiones.
- Revisión de código con enfoque defensivo y ofensivo.

El proyecto está pensado para **laboratorios locales y despliegue en VPS**, donde se puede analizar tráfico, endurecer configuraciones y evaluar riesgos reales.

---

## 2. Descripción detallada de los scripts

### `client.py`
- **Funcionalidad**: Cliente de chat con GUI (`tkinter`) que se conecta a un servidor remoto mediante TLS, envía mensajes y recibe respuestas en tiempo real.
- **Problema que resuelve**: Permite  comunicaciones cifradas contra un servidor TLS y validar comportamiento del cliente frente a múltiples usuarios.
- **Escenarios profesionales**:
  - Comunicaciones Seguras
  - Pruebas de clientes mal configurados frente a MITM.
- **Suposiciones importantes**:
  - El host y puerto deben coincidir con el servidor (local o VPS).
  - Uso exclusivo en entornos controlados.
---

### `server.py`
- **Funcionalidad**: Servidor de chat TLS multi‑cliente con manejo concurrente mediante hilos.
- **Problema que resuelve**: Proporciona un backend cifrado para pruebas de comunicación segura entre múltiples clientes.
- **Escenarios profesionales**:
  - Hardening de servicios TLS.
  - Análisis de concurrencia y gestión de sesiones.
  - Auditoría de servidores de red sencillos.
- **Suposiciones importantes**:
  - Requiere claves y certificado TLS propios.
  - No implementa autenticación ni control de acceso.
  - No apto para producción sin endurecimiento.

---

## 3. Requisitos técnicos
- Python 3.x
- Acceso a shell en sistema Linux (local o VPS)
- Módulos estándar: `socket`, `ssl`, `threading`, `tkinter`
- Certificado y clave TLS en el servidor

---

## 4. Creación de un certificado TLS (servidor)

###  Crear el archivo de configuración `openssl.cnf`

Define para qué nombre o IP será válido el certificado mediante **Subject Alternative Name (SAN)**:

```ini
[ req ]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = req_ext

[ dn ]
CN = localhost

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = localhost
# IP.1 = 203.0.113.10   # opcional
````
###  Generar el certificado y el par de claves 
Con un solo comando, OpenSSL genera automáticamente el par de claves y el certificado:
````init
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout server-key.key \
  -out server-cert.pem \
  -config openssl.cnf
````

🖥️ Servidor: usa `server-key.key` + `server-cert.pem`

💻 Cliente: copia solo `server-cert.pem` para validar al servidor

## 5. Ejecuion y usos
````bash
python3 server.py
````

````bash
python3 cliente.py
````

<img width="1908" height="891" alt="image" src="https://github.com/user-attachments/assets/4bb7f7ce-aaa3-4d74-9daf-016b4e5444c5" />

