import os
import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


class ResendEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        resend.api_key = os.getenv("RESEND_API_KEY")

    def send_messages(self, email_messages):
        sent_count = 0
        for message in email_messages:
            try:
                from_email = sanitize_address(message.from_email, message.encoding)
                to_emails = [sanitize_address(addr, message.encoding) for addr in message.recipients()]

                # Plain text body
                text_body = message.body

                # HTML body (if exists in alternatives)
                html_body = None
                for alt, mimetype in getattr(message, "alternatives", []):
                    if mimetype == "text/html":
                        html_body = alt
                        break

                resend.Emails.send({
                    "from": from_email,
                    "to": to_emails,
                    "subject": message.subject,
                    "text": text_body,
                    "html": html_body or text_body,  # fallback if no HTML
                })
                sent_count += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return sent_count
