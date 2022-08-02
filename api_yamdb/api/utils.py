from random import randint

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail


def send_code(user):
    '''Sending Confirmation Code'''
    
    number = randint(1000000, 10000000)
    confirmation_code = str(number) + str(user.username)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Confirmation_code',
        message=f'Your confirmation_code is: {confirmation_code}',
        from_email={DEFAULT_FROM_EMAIL},
        recipient_list=[user.email],
        fail_silently=False,
    )
