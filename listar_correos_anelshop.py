
import imaplib
import email

# Datos de la cuenta de Gmail
EMAIL_USER = "anel3936@gmail.com"  # Reemplaza con tu correo de Gmail
EMAIL_PASS = "iewl qjjs nsul qdzv"  # Reemplaza con tu contraseña
IMAP_SERVER = "imap.gmail.com"

# Función para limpiar la contraseña (eliminar espacios)
def limpiar_contraseña(contraseña):
    return contraseña.replace(' ', '')

# Función para conectar a la cuenta de Gmail usando IMAP
def conectar_imap():
    # Limpiar la contraseña
    password = limpiar_contraseña(EMAIL_PASS)
    
    # Conexión al servidor IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, password.encode('utf-8'))  # Asegurándonos de que la contraseña sea en formato bytes
    return mail

# Función para listar los correos de la cuenta de Gmail de @anelshop.com
def listar_correos():
    mail = conectar_imap()
    
    # Seleccionar la bandeja de entrada
    mail.select("inbox")
    
    # Buscar correos solo de @anelshop.com
    status, mensajes = mail.search(None, 'FROM', '"@anelshop.com"')  # Filtro para correos de anelshop.com
    
    # Imprimir todos los correos
    if status == "OK":
        for num in mensajes[0].split():
            status, datos = mail.fetch(num, "(RFC822)")
            for response_part in datos:
                if isinstance(response_part, tuple):
                    mensaje = email.message_from_bytes(response_part[1])
                    print("De:", mensaje["From"])
                    print("Asunto:", mensaje["Subject"])
                    print("Fecha:", mensaje["Date"])
                    print("-" * 50)
    else:
        print("No se encontraron correos de @anelshop.com.")
        
# Ejecutar la función de listar correos
listar_correos()
