from .models import *
from .serializers import *
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


def ActivateEmail(security, domain, user, to_email):
    try:
        mail_subject = 'Activate your user account.'
        html_message = render_to_string('activate_account.html', {
            'subject': 'Account activation',
            'user': user['first_name'], 
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user['pk'])),
            'token': account_activation_token.make_token(user),
            'protocol': security
        })
        plain_message = strip_tags(html_message)  
        message = EmailMultiAlternatives(
            subject = mail_subject, 
            body = plain_message,
            to= [to_email]
        )
    
        message.attach_alternative(html_message, "text/html")
        message.send()
        return {"message":"Please confirm your email address to complete the registration"}
    except Exception as e:
        raise Exception(e) 