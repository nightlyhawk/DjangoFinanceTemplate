from django.db import models
from user.models import NewUser

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(NewUser, on_delete=models.CASCADE, related_name='account')
    transfers = models.IntegerField(default=0)
    balance = models.IntegerField(default=100000)

    def __str__(self):
        return self.user.full_name

class Transfer(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sending_transfer')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiving_transfer')
    amount = models.IntegerField(default=0)

    def __str__(self):
        return "from " + self.sender.user.full_name + " to " + self.receiver.user.full_name
