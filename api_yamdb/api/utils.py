import uuid
from random import randint
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

def send_code(email, user):
    # confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)
    number = randint(10000, 100000)
    confirmation_code = str(number) + str(email)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Код confirmation_code',
        message=f'Your confirmation_code is: {confirmation_code}',
        from_email={DEFAULT_FROM_EMAIL},
        recipient_list=[email],
        fail_silently=False,
    )