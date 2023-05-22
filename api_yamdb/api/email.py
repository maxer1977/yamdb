from django.core.mail import EmailMessage


def send_email_message(body, to):
    """Отправка сообщения с токеном пользователю."""
    email = EmailMessage(
        subject='Доступ к API:',
        body=body,
        to=[to]
    )
    email.send()
