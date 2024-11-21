from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
import logging
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
attachment_basic_path = os.path.dirname("app.static")

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)

async def send_confirmation_email(email_to: str, ticket_info: dict, attachment_path: str = None):
    body_content = f"""
    <h2>Confirmación de Registro - {ticket_info.get('event_name')} - Temporada de Estrenos ASAB</h2>
    <p>¡Hola!, tu registro para la función de <b>{ticket_info.get('event_name')}</b> ha sido confirmado.</p>
    <p>A continuación la información de tu registro:</p>
    <ul>
        <li><b>Nombre:</b> {ticket_info.get('ticket_name')}</li>
        <li><b>Evento:</b> {ticket_info.get('event_name')}</li>
        <li><b>Fecha:</b> {ticket_info.get('event_date')}</li>
        <li><b>Hora:</b> {ticket_info.get('event_time')}</li>
        <li><b>Lugar:</b> {ticket_info.get('stage_name')} - {ticket_info.get('stage_address')}</li>
        <!-- Añadir más información si es necesario -->
    </ul>
    <h2>Recomendaciones de ingreso a la función</h2>
    <ul>
        <li>Recuerda llegar mínimo con <b>15 minutos de anticipación</b> a la hora de la función para validar tu entrada.</li>
        <li>Por cuestiones de aforo, <b>solamente podemos reservar tu entrada hasta 15 minutos antes de la hora de función</b> después se comienza a dar registro a las personas que están en sala esperando ingreso hasta completar el total del aforo.</li>
        <li>El ingreso a sala se realiza <b>10 minutos antes de la hora de función</b> no se permitirá el ingreso después de esa hora.</li>
    </ul>
    <p>¡Gracias por tu participación!</p>
    <br>
    <p>----------------------</p>
    <br>
    <p>Sistema de Caracterización de Públicos para las Artes Escénicas</p>
    <p>Proyecto de Investigación "Análisis de la escenificación como fuente de análisis crítico y la evaluación formativa"</p>
    <p>Grupo de Investigación Dramaturgias del cuerpo y Escrituras del Espacio / Grupo de Investigación Áulide.</p>
    <p>Factultad de Artes ASAB - UDFJC </p>
    """

    # Obtener el directorio actual (app/email) y luego resolver hacia app/static
    current_directory = os.path.dirname(os.path.abspath(__file__))  # app/email
    static_directory = os.path.abspath(os.path.join(current_directory, "../static"))

    # Construir la ruta completa del archivo en app/static
    attachment_path = os.path.join(static_directory, "flyer_witches.jpg") #falta actualizar para que se envíe el flyer segun cada evento
    #print(attachment_path)

    message = MessageSchema(
        subject=f"Confirmacion de Registro - {ticket_info.get('event_name')}",
        recipients=[email_to],
        body=body_content,
        subtype="html",
        bcc=["info@estudiocajanegra.net"],
        attachments=[attachment_path] if attachment_path else None 
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logging.info(f"Correo de confirmación enviado a {email_to}")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email_to}: {e}")


async def send_survey_email(email_to: str, ticket_info: dict):
    body_content = f"""
    <h2>¿Qué opinas de {ticket_info.get('event_name')}? - Temporada de Estrenos ASAB</h2>
    <p>¡Hola!</p>
    <p>Muchas gracias por acompañarnos en la función de <b>{ticket_info.get('event_name')}</b>. Nos encantaría conocer tu percepción sobre el espectáculo, y para ello, hemos preparado una breve encuesta.</p>
    <p>Tu participación es <strong>completamente anónima</strong>, y tus respuestas serán manejadas de manera <strong>confidencial</strong>, utilizándose únicamente con fines académicos y de investigación.</p>
    <p><a href="https://cornflowerblue-hyena-638150.hostingersite.com/bwitches-encuesta/">👉 HAZ CLIC AQUÍ PARA DILIGENCIAR LA ENCUESTA 👈</a><br><br></p>
    <p>Esta encuesta forma parte del proyecto de investigación <strong>"Análisis de la escenificación"</strong> en el área de <strong>Públicos</strong>, desarrollado por el <strong>Grupo de Investigación Dramaturgias del Cuerpo y Escrituras del Espacio</strong> y el <strong>Grupo de Investigación Áulide</strong>, en la Facultad de Artes ASAB.<b>Grupo de Investigación Dramaturgias del Cuerpo y Escrituras del Espacio</b> y el <b>Grupo de Investigación Áulide</b>.</p>
    <p>Nuestro objetivo es entender mejor la percepción de los asistentes a las funciones teatrales de la <strong>Temporada de Estrenos</strong> y construir conocimiento sobre la relación entre las artes escénicas y su público.</p>
    <p><strong>¡Gracias por ayudarnos a dar vida al teatro desde una perspectiva académica y crítica!</strong></p></p>
    <br>
    <p>----------------------</p>
    <br>
    <p style="font-size: 14px; color: #555;">
            <strong>Sistema de Caracterización de Públicos para las Artes Escénicas</strong><br>
            Proyecto de Investigación: <em>"Análisis de la escenificación como fuente de análisis crítico y evaluación formativa"</em><br>
            Grupos de Investigación: Dramaturgias del Cuerpo y Escrituras del Espacio / Áulide<br>
            <strong>Facultad de Artes ASAB – UDFJC</strong>
        </p>
    """

    message = MessageSchema(
        subject=f"¿Qué opinas de {ticket_info.get('event_name')}?",
        recipients=[email_to],
        body=body_content,
        subtype="html",
        bcc=["info@estudiocajanegra.net"],
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logging.info(f"Correo Survey enviado a {email_to}")
    except Exception as e:
        logging.error(f"Error al enviar correo Survey a {email_to}: {e}")