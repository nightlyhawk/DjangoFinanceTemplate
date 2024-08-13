from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomAccountManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=100, default='pin')
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, default='earth')
    full_name =  models.CharField(max_length=100, default='')
    tag = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class Profile(models.Model): 
    user = models.OneToOneField(NewUser, on_delete= models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profile/', null=True, blank=True)
    d_o_b = models.DateField(auto_now=False, null=True)
    phone_no = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200,)
    upload_id = models.ImageField(upload_to='user_id/', null=True, blank=True)
 
    def __str__(self):
        return self.user.first_name
    
