import os
import base64
from pathlib import Path
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition

load_dotenv()  # carga variables desde .env

api_key = os.environ.get("SENDGRID_API_KEY")
if not api_key:
    raise RuntimeError("Falta SENDGRID_API_KEY en el entorno")

sg = sendgrid.SendGridAPIClient(api_key=api_key)

from_email = Email("antonio.vitalic@conergie.cl")
to = To("antoninte99@gmail.com")
subject = "My SendGrid Message"
content = Content("text/html", "Hello <b>friend!</b>")
mail = Mail(from_email, to, subject, content)

pdf_path = Path(__file__).parent / "cv.pdf"
with open(pdf_path, "rb") as f:
    data = f.read()

encoded_file = base64.b64encode(data).decode()

attached_file = Attachment(
    FileContent(encoded_file),
    FileName("cv.pdf"),
    FileType("application/pdf"),
    Disposition("attachment")
)

mail.attachment = attached_file
mail_json = mail.get()

response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)