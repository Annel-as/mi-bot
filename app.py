from flask import Flask, request, jsonify
import imaplib
import email
from email.header import decode_header

app = Flask(__name__)

# Configuración del servidor IMAP
EMAIL_ACCOUNT = "anel3936@gmail.com"
EMAIL_PASSWORD = "iewl qjjs nsul qdzv"  # Contraseña de aplicación
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993

@app.route('/buscar-correo', methods=['POST'])
def buscar_correo():
    # Obtener el correo a filtrar desde el cuerpo de la solicitud
    data = request.get_json()
    CORREO = data.get("correo")
    if not CORREO:
        print("Error: El campo 'correo' es obligatorio.")
        return jsonify({"error": "El campo 'correo' es obligatorio"}), 400

    try:
        print("Intentando conectar al servidor IMAP...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print("Conexión exitosa.")

        # Seleccionar la bandeja de entrada
        print("Seleccionando bandeja de entrada...")
        mail.select("inbox")

        # Buscar todos los correos electrónicos
        print("Buscando correos electrónicos...")
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("Error: No se pudieron recuperar los correos.")
            return jsonify({"error": "No se pudieron recuperar los correos"}), 500

        # Obtener las IDs de los correos
        email_ids = messages[0].split()
        print(f"Se encontraron {len(email_ids)} correos.")

        # Procesar solo los 50 correos más recientes
        email_ids = email_ids[-50:]  # Tomar los últimos 50 correos
        print(f"Procesando los últimos {len(email_ids)} correos.")

        # Iterar sobre cada correo
        for email_id in reversed(email_ids):  # Procesar en orden descendente
            print(f"\nProcesando correo con ID: {email_id.decode()}")
            # Obtener el correo
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                print(f"Error al obtener el correo con ID: {email_id.decode()}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Analizar el correo
                    msg = email.message_from_bytes(response_part[1])
                    # Obtener el destinatario
                    to_ = msg.get("To")
                    if to_:
                        to_ = to_.strip("<>").strip()  # Normalizar el destinatario
                    print(f"Destinatario normalizado: {to_}")

                    # Inicializar una variable para indicar si el destinatario fue encontrado
                    destinatario_encontrado = False

                    # Filtrar por el destinatario en los encabezados
                    if to_ and CORREO in to_:
                        destinatario_encontrado = True
                        print(f"El correo coincide con el destinatario filtrado en los encabezados: {CORREO}")

                    # Si no se encuentra en los encabezados, buscar en el cuerpo
                    if not destinatario_encontrado:
                        print("Buscando el destinatario en el cuerpo del correo...")
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":  # Buscar solo en texto plano
                                    try:
                                        body = part.get_payload(decode=True).decode()
                                        print(f"Contenido del cuerpo del correo: {body}")
                                        if CORREO in body:
                                            destinatario_encontrado = True
                                            print(f"El destinatario {CORREO} fue encontrado en el cuerpo del correo.")
                                            break
                                    except Exception as e:
                                        print(f"Error al decodificar el contenido: {e}")
                        else:
                            content_type = msg.get_content_type()
                            if content_type == "text/plain":
                                try:
                                    body = msg.get_payload(decode=True).decode()
                                    print(f"Contenido del cuerpo del correo: {body}")
                                    if CORREO in body:
                                        destinatario_encontrado = True
                                        print(f"El destinatario {CORREO} fue encontrado en el cuerpo del correo.")
                                except Exception as e:
                                    print(f"Error al decodificar el contenido: {e}")

                    # Si el destinatario fue encontrado, devolver el contenido del correo
                    if destinatario_encontrado:
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        from_ = msg.get("From")
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        print("\nCorreo encontrado:")
                        print(f"Asunto: {subject}")
                        print(f"Remitente: {from_}")
                        print(f"Destinatario: {to_}")
                        print(f"Contenido: {body}")

                        # Cerrar conexión
                        mail.logout()
                        return jsonify({
                            "asunto": subject,
                            "remitente": from_,
                            "destinatario": to_,
                            "contenido": body
                        })

        # Si no se encontró ningún correo
        print("No se encontró ningún correo con el destinatario especificado.")
        mail.logout()
        return jsonify({"error": "No se encontró ningún correo con el destinatario especificado"}), 404

    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/buscar-correo_amazon', methods=['POST'])
def buscar_correo_amazon():
    try:
        print("Intentando conectar al servidor IMAP...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        print("Conexión exitosa.")

        # Seleccionar la bandeja de entrada
        print("Seleccionando bandeja de entrada...")
        mail.select("inbox")

        # Buscar todos los correos electrónicos
        print("Buscando correos electrónicos...")
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            print("Error: No se pudieron recuperar los correos.")
            return jsonify({"error": "No se pudieron recuperar los correos"}), 500

        # Obtener las IDs de los correos
        email_ids = messages[0].split()
        print(f"Se encontraron {len(email_ids)} correos.")

        # Procesar solo los 50 correos más recientes
        email_ids = email_ids[-50:]  # Tomar los últimos 50 correos
        print(f"Procesando los últimos {len(email_ids)} correos.")

        # Iterar sobre cada correo
        for email_id in reversed(email_ids):  # Procesar en orden descendente
            print(f"\nProcesando correo con ID: {email_id.decode()}")
            # Obtener el correo
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            if status != "OK":
                print(f"Error al obtener el correo con ID: {email_id.decode()}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Analizar el correo
                    msg = email.message_from_bytes(response_part[1])
                    # Buscar en el cuerpo del correo
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":  # Buscar solo en texto plano
                                try:
                                    body = part.get_payload(decode=True).decode()
                                    print(f"Contenido del cuerpo del correo: {body}")
                                    if "Alguien que conoce tu contraseña está intentando ingresar a tu cuenta." in body:
                                        # Extraer información del correo
                                        subject, encoding = decode_header(msg["Subject"])[0]
                                        if isinstance(subject, bytes):
                                            subject = subject.decode(encoding if encoding else "utf-8")
                                        from_ = msg.get("From")
                                        to_ = msg.get("To")
                                        print("\nCorreo encontrado:")
                                        print(f"Asunto: {subject}")
                                        print(f"Remitente: {from_}")
                                        print(f"Destinatario: {to_}")
                                        print(f"Contenido: {body}")

                                        # Cerrar conexión
                                        mail.logout()
                                        return jsonify({
                                            "asunto": subject,
                                            "remitente": from_,
                                            "destinatario": to_,
                                            "contenido": body
                                        })
                                except Exception as e:
                                    print(f"Error al decodificar el contenido: {e}")
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            try:
                                body = msg.get_payload(decode=True).decode()
                                print(f"Contenido del cuerpo del correo: {body}")
                                if "Alguien que conoce tu contraseña está intentando ingresar a tu cuenta." in body:
                                    # Extraer información del correo
                                    subject, encoding = decode_header(msg["Subject"])[0]
                                    if isinstance(subject, bytes):
                                        subject = subject.decode(encoding if encoding else "utf-8")
                                    from_ = msg.get("From")
                                    to_ = msg.get("To")
                                    print("\nCorreo encontrado:")
                                    print(f"Asunto: {subject}")
                                    print(f"Remitente: {from_}")
                                    print(f"Destinatario: {to_}")
                                    print(f"Contenido: {body}")

                                    # Cerrar conexión
                                    mail.logout()
                                    return jsonify({
                                        "asunto": subject,
                                        "remitente": from_,
                                        "destinatario": to_,
                                        "contenido": body
                                    })
                            except Exception as e:
                                print(f"Error al decodificar el contenido: {e}")

        # Si no se encontró ningún correo
        print("No se encontró ningún correo con el texto especificado.")
        mail.logout()
        return jsonify({"error": "No se encontró ningún correo con el texto especificado"}), 404

    except Exception as e:
        print(f"Error inesperado: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Iniciando la aplicación Flask...")
    app.run(debug=True)