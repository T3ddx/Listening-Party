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

    @staticmethod
    def get_party_invites(username):
        return Party_Invite.objects.get_queryset().filter(inviter=Users.objects.get(username=username))

class Party(models.Model):
    name = models.CharField(max_length=50)
    party_leader = models.ForeignKey(Users, blank=True, null=True, on_delete=models.CASCADE, related_name='party_leader')
    users = models.ManyToManyField(Users, blank=True)
    invites = models.ManyToManyField(Party_Invite, blank=True)

    def __str__(self):
        return self.name

    def is_party_leader(self, user):
        return self.party_leader == user

    def is_member(self, user):
        for member in self.users:
            if member == user:
                return True
        return False

    def remove_and_rearrange(self, user):
        pass

    @staticmethod
    def get_current_party(user):
        search_for_member = Party.objects.all().filter(users__username=user.username)
        search_for_leader = Party.objects.all().filter(party_leader=user)
        
        if search_for_member:
            return search_for_member.get()
        
        if search_for_leader:
            return search_for_leader.get()

        return None