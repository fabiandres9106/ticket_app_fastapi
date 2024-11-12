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
    <h2>Encuesta de Percepción del Espectador - {ticket_info.get('event_name')} - Temporada de Estrenos ASAB</h2>
    <p>¡Hola!, gracias por participar en la función de <b>{ticket_info.get('event_name')}</b>.</p>
    <p>En el siguiente link encontrarás una encuesta enfocada a concer tu percepción sobre el espectáculo. La encuesta es completamente anónima, te aseguramos que tus respuestas serán almacenadas de forma confidencial y utilizadas únicamente con fines académicos e investigativos:</p>
    <p><a href="https://cornflowerblue-hyena-638150.hostingersite.com/bwitches-encuesta/">PARA DILIGENCIAR LA ENCUESTA, HAZ CLIC AQUÍ</a><br><br></p>
    <p>Esta encuesta hace parte del proyecto de investigación Análisis de la escenificación en el área de Públicos del <b>Grupo de Investigación Dramaturgias del Cuerpo y Escrituras del Espacio</b> y el <b>Grupo de Investigación Áulide</b>. Estamos interesados en conocer la percepción de los asistentes a las funciones teatrales en la Temporada de Estrenos de la Facultad de Artes ASAB.</p>
    <p><strong>¡Gracias por ayudarnos a construir el conocimiento sobre los espectadores teatrales de la Temporada de Estrenos ASAB!</strong></p></p>
    <br>
    <p>----------------------</p>
    <br>
    <p>Sistema de Caracterización de Públicos para las Artes Escénicas</p>
    <p>Proyecto de Investigación "Análisis de la escenificación como fuente de análisis crítico y la evaluación formativa"</p>
    <p>Grupo de Investigación Dramaturgias del cuerpo y Escrituras del Espacio / Grupo de Investigación Áulide.</p>
    <p>Factultad de Artes ASAB - UDFJC </p>
    """

    message = MessageSchema(
        subject=f"Encuesta de Percepción del Espectador - {ticket_info.get('event_name')}",
        recipients=[email_to],
        body=body_content,
        subtype="html",
        bcc=["info@estudiocajanegra.net"],
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logging.info(f"Correo de confirmación enviado a {email_to}")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email_to}: {e}")