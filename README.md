# FyisBot v3 🎬

Sistema de gestión de códigos de hogar Netflix con panel de administración de tokens.

## Características

- 🔐 Sistema de autenticación por tokens
- ⚙️ Panel de administración (token admin: 152028)
- 🎫 Generación de tokens personalizados con expiración
- 📧 Búsqueda de correos de Netflix en cuentas IMAP
- 🔗 Extracción automática de links
- ⏰ Advertencia de expiración de links (15 minutos)
- 🎨 Interfaz moderna con diseño glassmorphism

## Instalación

1. Clona el repositorio:
```bash
git clone <tu-repositorio>
cd fyisbot-v3/fyisbot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno en `.env`:
```env
FYIS_SECRET_KEY=tu_clave_secreta
FYIS_ACCOUNTS={"correo@gmail.com":"contraseña_imap"}
```

4. Ejecuta la aplicación:
```bash
python app.py
```

## Uso

### Acceso Admin
- Usa el token `152028` para acceder al panel de administración
- Desde ahí puedes crear, ver y eliminar tokens de usuarios

### Acceso Usuario
- Ingresa con un token generado por el admin
- Busca correos ingresando el email de la cuenta Netflix
- Visualiza los códigos con sus links y tiempo de expiración

## Despliegue en Vercel

1. Sube el proyecto a GitHub (asegúrate de que `.env` no se suba)
2. Conecta el repositorio en Vercel
3. Configura las variables de entorno en Vercel:
   - `FYIS_SECRET_KEY`
   - `FYIS_ACCOUNTS`
4. Despliega automáticamente

## Tecnologías

- Flask (Backend)
- Python 3.x
- IMAP (Gmail)
- BeautifulSoup4 (Parsing HTML)
- HTML/CSS (Frontend)

## Notas

- Los tokens se almacenan en memoria (considera usar una base de datos en producción)
- Los links de Netflix expiran 15 minutos después del envío
- Requiere contraseñas de aplicación de Google para IMAP

---
Desarrollado por Fyis 🚀
