import smtplib

from django.conf import settings


def send_new_password_email(new_password_request):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(settings.SENDING_EMAIL, settings.SENDING_EMAIL_PASSWORD)

    message = "\r\n".join([
        f"From: {settings.SENDING_EMAIL}",
        f"To: {new_password_request.email}",
        "Subject: New Password Request",
        "",
        f"""
            Hello, 

            You requested a new password.  Click the link below to enter create a new password

            {settings.VERIFICATION_DOMAIN}/new-password/{new_password_request.id}

            If you did not request this you can ignore this email.

            Kind regards,
            Email Collect
            """
    ])

    server.sendmail(settings.SENDING_EMAIL, new_password_request.email, message)

    server.close()
