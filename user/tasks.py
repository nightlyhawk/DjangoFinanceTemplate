from celery import shared_task
from .services import ActivateEmail

@shared_task
def activate_email(security, domain, user, email):
    status = ActivateEmail(security, domain, user, email)
    return status
