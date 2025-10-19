
from django.core.mail import send_mail
from django.conf import settings

def send_order_email(subject: str, message: str, recipient_list: list):
    """
    Uses configured SMTP backend. Raises on failure so Vercel logs show errors.
    """
    send_mail(
        subject,
        message,
        getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list,
        fail_silently=False,
    )