import imaplib, email, pytz, os, json, re, secrets
from email.header import decode_header
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

app = Flask(__name__)
application = app
app.secret_key = os.getenv('FYIS_SECRET_KEY', 'fyisbot_default_secret')

TOKEN_ADMIN = "152028"
CUENTAS_ACCESO = json.loads(os.getenv('FYIS_ACCOUNTS', '{}'))

# Mapeo de correos de dominio a cuentas Gmail
MAPEO_CORREOS = {
    "karolombardi@mypemx.com": "hgm2748@gmail.com",
    "eduardo@mypemx.com": "hgm2748@gmail.com",
    "netflix00800@mypemx.com": "hgm2748@gmail.com",
    "netflix09002@mypemx.com": "hgm2748@gmail.com",
    "netflix66333@mypemx.com": "hgm2748@gmail.com",
    "netflix8330@mypemx.com": "mhg91984@gmail.com",
    "netflix7473@mypemx.com": "mhg91984@gmail.com"
}

# Archivo para persistir tokens
TOKENS_FILE = 'tokens_data.json'

# Cargar tokens desde variable de entorno o archivo
def cargar_tokens():
    # Primero intentar cargar desde variable de entorno (para Vercel)
    tokens_env = os.getenv('FYIS_TOKENS')
    if tokens_env:
        try:
            return json.loads(tokens_env)
        except:
            pass
    
    # Si no hay en variable de entorno, intentar desde archivo local
    try:
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

# Guardar tokens (solo en archivo local, en Vercel usar variable de entorno)
def guardar_tokens():
    try:
        with open(TOKENS_FILE, 'w') as f:
            json.dump(tokens_generados, f, indent=2)
        # Imprimir para que puedas copiar y pegar en Vercel
        print("="*50)
        print("TOKENS ACTUALIZADOS - Copia esto en Vercel como FYIS_TOKENS:")
        print(json.dumps(tokens_generados, indent=2))
        print("="*50)
    except Exception as e:
        print(f"Error guardando tokens: {e}")

# Almacenamiento de tokens generados (persistente)
tokens_generados = cargar_tokens()

# Inicializar con token por defecto si está vacío
if not tokens_generados:
    tokens_generados = {
        'code02': {
            'token': 'code02',
            'creado': '28/02/2026 12:00 PM',
            'expira': False,
            'usado': 0
        }
    }

ASUNTOS_NETFLIX = [
    "Netflix: Tu código de inicio de sesión",
    "Importante: Cómo actualizar tu Hogar con Netflix",
    "Tu código de acceso temporal de Netflix",
    "Importante: Cómo cambiar tu hogar Netflix"
]

def extraer_link_netflix(cuerpo_html):
    """Extrae el link principal del correo de Netflix"""
    try:
        soup = BeautifulSoup(cuerpo_html, 'html.parser')
        # Buscar links que contengan netflix.com
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'netflix.com' in href and 'account' in href:
                return href
        # Si no encuentra, buscar cualquier link de Netflix
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'netflix.com' in href:
                return href
        return None
    except:
        return None

def calcular_expiracion(fecha_envio):
    """Calcula si el link ya expiró (15 minutos después del envío)"""
    try:
        peru_tz = pytz.timezone('America/Lima')
        ahora = datetime.now(peru_tz)
        dt_envio = email.utils.parsedate_to_datetime(fecha_envio).astimezone(peru_tz)
        tiempo_expiracion = dt_envio + timedelta(minutes=15)
        minutos_restantes = (tiempo_expiracion - ahora).total_seconds() / 60
        return {
            'expirado': minutos_restantes <= 0,
            'minutos_restantes': max(0, int(minutos_restantes)),
            'hora_expiracion': tiempo_expiracion.strftime('%I:%M %p')
        }
    except:
        return {'expirado': False, 'minutos_restantes': 15, 'hora_expiracion': 'N/A'}

def obtener_hora_peru(fecha_raw):
    try:
        dt = email.utils.parsedate_to_datetime(fecha_raw)
        peru_tz = pytz.timezone('America/Lima')
        return dt.astimezone(peru_tz).strftime('%d/%m/%Y %I:%M %p')
    except: return fecha_raw

def escanear_veloz(correo_cliente):
    resultados = []
    peru_tz = pytz.timezone('America/Lima')
    fecha_busqueda = (datetime.now(peru_tz) - timedelta(days=1)).strftime("%d-%b-%Y")
    
    # Determinar en qué Gmail buscar según el mapeo
    correo_normalizado = correo_cliente.lower().strip()
    cuentas_a_buscar = {}
    
    if correo_normalizado in MAPEO_CORREOS:
        # Si el correo está en el mapeo, buscar solo en ese Gmail específico
        gmail_target = MAPEO_CORREOS[correo_normalizado]
        if gmail_target in CUENTAS_ACCESO:
            cuentas_a_buscar[gmail_target] = CUENTAS_ACCESO[gmail_target]
    else:
        # Si no está en el mapeo, buscar en todas las cuentas (comportamiento por defecto)
        cuentas_a_buscar = CUENTAS_ACCESO
    
    for cuenta, clave in cuentas_a_buscar.items():
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(cuenta, clave)
            mail.select("inbox")
            search_query = f'(FROM "info@account.netflix.com" SINCE {fecha_busqueda})'
            status, messages = mail.search(None, search_query)
            ids = messages[0].split()[-10:][::-1]  # Buscar últimos 10 correos
            for i in ids:
                res, data = mail.fetch(i, "(RFC822)")
                for response in data:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        destinatario = str(msg.get("To", "")).lower()
                        if correo_cliente.lower() not in destinatario:
                            continue
                        subject, enc = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes): subject = subject.decode(enc or "utf-8")
                        if any(s.lower() in subject.lower() for s in ASUNTOS_NETFLIX):
                            cuerpo = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/html":
                                        cuerpo = part.get_payload(decode=True).decode()
                                        break
                            else: cuerpo = msg.get_payload(decode=True).decode()
                            
                            link = extraer_link_netflix(cuerpo)
                            fecha_raw = msg["Date"]
                            expiracion = calcular_expiracion(fecha_raw)
                            
                            resultados.append({
                                "bandeja": correo_cliente,
                                "subject": subject,
                                "date": obtener_hora_peru(fecha_raw),
                                "link": link,
                                "expiracion": expiracion
                            })
            mail.logout()
        except Exception as e:
            print(f"Error con la cuenta {cuenta}: {e}")
            continue
    return resultados

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token = request.form.get('token')
        if token == TOKEN_ADMIN:
            session['is_admin'] = True
            session['auth'] = True
            return redirect(url_for('admin_panel'))
        elif token in tokens_generados:
            token_data = tokens_generados[token]
            # Verificar si el token no ha expirado
            if token_data['expira']:
                if datetime.now() > datetime.fromisoformat(token_data['fecha_expiracion']):
                    return render_template('login.html', error="Token expirado")
            # Incrementar contador de usos
            tokens_generados[token]['usado'] = tokens_generados[token].get('usado', 0) + 1
            session['auth'] = True
            session['is_admin'] = False
            session['token'] = token
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Token inválido")
    return render_template('login.html', error=None)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    
    mensaje = None
    
    if request.method == 'POST':
        accion = request.form.get('accion')
        
        if accion == 'crear':
            # Permitir token personalizado o generar uno aleatorio
            token_nuevo = request.form.get('token_personalizado', '').strip()
            if not token_nuevo:
                token_nuevo = secrets.token_hex(4)  # Token de 8 caracteres
            elif token_nuevo in tokens_generados:
                mensaje = f"El token '{token_nuevo}' ya existe. Usa otro."
                return render_template('admin.html', tokens=tokens_generados, mensaje=mensaje)
            
            expira = request.form.get('expira') == 'si'
            
            token_info = {
                'token': token_nuevo,
                'creado': datetime.now().strftime('%d/%m/%Y %I:%M %p'),
                'expira': expira,
                'usado': 0
            }
            
            if expira:
                dias = int(request.form.get('dias', 7))
                fecha_exp = datetime.now() + timedelta(days=dias)
                token_info['fecha_expiracion'] = fecha_exp.isoformat()
                token_info['dias'] = dias
            
            tokens_generados[token_nuevo] = token_info
            guardar_tokens()  # Persistir cambios
            mensaje = f"Token {token_nuevo} creado exitosamente"
        
        elif accion == 'eliminar':
            token_eliminar = request.form.get('token_eliminar')
            if token_eliminar in tokens_generados:
                del tokens_generados[token_eliminar]
                guardar_tokens()  # Persistir cambios
                mensaje = "Token eliminado"
    
    return render_template('admin.html', tokens=tokens_generados, mensaje=mensaje)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('auth'):
        return redirect(url_for('login'))
    mails = []
    busqueda_realizada = False
    last_email = None
    if request.method == 'POST':
        busqueda_realizada = True
        last_email = request.form.get('email')
        mails = escanear_veloz(last_email)
    return render_template('dashboard.html', mails=mails, busqueda=busqueda_realizada, last_email=last_email)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
