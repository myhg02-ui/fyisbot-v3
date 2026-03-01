# 📧 Cómo Obtener Credenciales de Gmail para IMAP

## Paso 1: Habilitar Verificación en 2 Pasos

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Navega a **Seguridad** en el menú lateral
3. Busca **Verificación en 2 pasos** y actívala si no lo está
4. Sigue los pasos para configurarla (necesitarás tu teléfono)

## Paso 2: Generar Contraseña de Aplicación

1. Una vez activada la verificación en 2 pasos, regresa a **Seguridad**
2. Busca **Contraseñas de aplicaciones** (aparece solo si tienes 2FA activo)
3. Haz clic en **Contraseñas de aplicaciones**
4. Selecciona:
   - **Aplicación**: Correo
   - **Dispositivo**: Otro (personalizado)
   - Ponle un nombre: "FyisBot" o "Netflix Bot"
5. Haz clic en **Generar**
6. **Copia la contraseña de 16 caracteres** (sin espacios)

## Paso 3: Configurar el .env

Edita tu archivo `.env` con:

```env
FYIS_SECRET_KEY=fyisbot_secret_2026_tu_clave_aleatoria
FYIS_ACCOUNTS={"tucorreo@gmail.com":"xxxx xxxx xxxx xxxx"}
```

**Importante**: 
- Reemplaza `tucorreo@gmail.com` con tu email real
- Reemplaza `xxxx xxxx xxxx xxxx` con la contraseña de aplicación generada
- Puedes agregar múltiples cuentas separadas por comas:
  ```json
  {"email1@gmail.com":"clave1","email2@gmail.com":"clave2"}
  ```

## Ejemplo Real

```env
FYIS_SECRET_KEY=mi_clave_super_secreta_2026
FYIS_ACCOUNTS={"fyis@gmail.com":"abcd efgh ijkl mnop"}
```

---

# 🚀 Deploy a GitHub y Vercel

## Paso 1: Preparar para GitHub

Tu proyecto ya tiene `.gitignore` que protege el archivo `.env`, así que estás listo.

## Paso 2: Subir a GitHub

```bash
# Inicializar git (si no lo has hecho)
cd "C:\Users\user\OneDrive\Escritorio\BOT IP HOGAR\fyisbot-v3\fyisbot"
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit - FyisBot v3"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/fyisbot-v3.git
git branch -M main
git push -u origin main
```

## Paso 3: Deploy en Vercel

### Opción A: Desde la Web de Vercel

1. Ve a https://vercel.com
2. Inicia sesión con GitHub
3. Haz clic en **New Project**
4. Importa tu repositorio `fyisbot-v3`
5. Configura las variables de entorno:
   - `FYIS_SECRET_KEY` = tu_clave_secreta
   - `FYIS_ACCOUNTS` = {"email@gmail.com":"contraseña_app"}
6. Haz clic en **Deploy**

### Opción B: Desde CLI de Vercel

```bash
# Instalar Vercel CLI
npm i -g vercel

# Desde la carpeta del proyecto
cd fyisbot
vercel

# Seguir los pasos y configurar variables de entorno
```

## Paso 4: Configurar Variables de Entorno en Vercel

**IMPORTANTE**: Debes agregar las variables de entorno en Vercel:

1. Ve a tu proyecto en Vercel Dashboard
2. Settings → Environment Variables
3. Agrega:
   - Name: `FYIS_SECRET_KEY`
   - Value: `tu_clave_secreta`
   
   - Name: `FYIS_ACCOUNTS`
   - Value: `{"email@gmail.com":"contraseña"}`

4. Haz clic en **Save**
5. Redeploy el proyecto para que tome las variables

## Paso 5: Dominio Personalizado (Opcional)

1. En Vercel Dashboard → Settings → Domains
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones de Vercel

---

## ⚠️ Checklist Antes de Deploy

- [ ] Archivo `.env` NO está en el repositorio (protegido por `.gitignore`)
- [ ] Variables de entorno configuradas en Vercel
- [ ] Contraseña de aplicación de Gmail generada correctamente
- [ ] `requirements.txt` tiene todas las dependencias
- [ ] Probado localmente con `python app.py`

---

## 🐛 Problemas Comunes

### "Authentication failed" en Gmail
- Verifica que la verificación en 2 pasos esté activa
- Genera una nueva contraseña de aplicación
- Asegúrate de copiar la contraseña sin espacios

### "Module not found" en Vercel
- Verifica que `requirements.txt` esté en la raíz del proyecto
- Asegúrate de que todas las dependencias estén listadas

### El bot no encuentra correos
- Verifica que el email en `FYIS_ACCOUNTS` sea correcto
- Asegúrate de que hay correos de Netflix recientes (últimas 24 horas)
- Revisa los logs en Vercel para ver errores

---

¿Listo para Deploy? 🚀
