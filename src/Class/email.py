import smtplib
from email.mime.text import MIMEText
from email.errors import MessageError, HeaderParseError
from msal import PublicClientApplication
import requests

class EmailSendOutlook:
    def __init__(self, client_id, tenant_id, username, password):
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.username = username
        self.password = password
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scopes = ["https://outlook.office365.com/.default"]
        self.access_token = None
    
    def validate_config(self, client_id, authority, scope):
        if not client_id:
            raise ValueError("El client_id es obligatorio.")
        if not authority.startswith("https://login.microsoftonline.com/"):
            raise ValueError("La authority debe apuntar a un endpoint válido de Azure AD.")
        if not isinstance(scope, list) or not scope:
            raise ValueError("Los scopes deben ser una lista no vacía.")
        
    def authenticate(self):
        """
        Autentica al usuario y obtiene un token de acceso.
        """
        try:
            self.validate_config(self.client_id, self.authority, self.scopes)
            app = PublicClientApplication(self.client_id, authority=self.authority)
            result = app.acquire_token_by_username_password(
                username=self.username,
                password=self.password,
                scopes=self.scopes,
            )
            if "access_token" in result:
                self.access_token = result["access_token"]
                print("Autenticación exitosa.")
            else:
                raise ValueError(f"Error de autenticación: {result['error']} - {result.get('error_description')}")
        except requests.exceptions.RequestException as e:
            print(f"Error de red: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def send_email(self, recipient, subject, body):
        """
        Envía un correo electrónico usando el token de autenticación.
        """
        try:
            self.authenticate()
            if not self.access_token:
                raise Exception("No se ha autenticado. validar su credencial de acceso. [client_id, tenant_id, username, password]")

            # Configuración del servidor SMTP
            smtp_server = "smtp.office365.com"
            smtp_port = 587
            sender = self.username

            # Configurar el mensaje
            msg = MIMEText(body)
            msg["From"] = sender
            msg["To"] = recipient
            msg["Subject"] = subject

            # Enviar el correo
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.docmd("AUTH XOAUTH2", f"user={sender}\x01auth=Bearer {self.access_token}\x01\x01")
                server.sendmail(sender, recipient, msg.as_string())
                print("Correo enviado exitosamente.")
                
        except HeaderParseError as e:
            print(f"Error al analizar el encabezado: {e}")
        except MessageError as e:
            print(f"Error general en el mensaje: {e}")
        except Exception as e:
            print(f"Otro error ocurrió: {e}")