from django.db import models
from login.models import Users
# Create your models here.
class Party_Invite(models.Model):
    party_name = models.CharField(max_length=50)
    invited = models.ForeignKey(Users, related_name='invited', on_delete=models.CASCADE)
    inviter = models.ForeignKey(Users, related_name='inviter', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.party_name}: {self.inviter} to {self.invited}'
    
    @staticmethod
    def get_invites(username):
        return Party_Invite.objects.get_queryset().filter(invited=Users.objects.get(username=username))

class Party(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(Users, blank=True)
    invites = models.ManyToManyField(Party_Invite, blank=True)
