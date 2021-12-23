import smtplib

from decouple import config


def send_mail(recipient_email, status, title):
    msg = f'Subject: Jobify\n\nYour apply to "{title}" ad is {status}.'
    sender = config('EMAIL')

    try:
        with smtplib.SMTP(config('EMAIL_HOST'), config('EMAIL_PORT')) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(sender, config('EMAIL_PASSWORD'))

            smtp.sendmail(sender, recipient_email, msg)

    except smtplib.SMTPAuthenticationError:
        pass
    except ConnectionRefusedError:
        pass
    except Exception:
        pass
