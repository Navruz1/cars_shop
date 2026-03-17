from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


def send_email_otp(email: str, otp_code: str, expires_at):
    subject = _("Your verification code")

    message = _(
        "Your one-time password (OTP) is: %(code)s\n\n"
        "This code will expire at %(expires)s.\n\n"
        "If you did not request this, please ignore this email."
    ) % {
        "code": otp_code,
        "expires": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,  # в dev пусть падает
    )


