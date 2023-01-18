from django.db import models
from login.models import Users
from time import sleep
# Create your models here.
class Party_Invite(models.Model):
    party_name = models.CharField(max_length=50)
    invited = models.ForeignKey(Users, related_name='invited', on_delete=models.CASCADE)
    inviter = models.ForeignKey(Users, related_name='inviter', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.party_name}: {self.inviter} to {self.invited}'
    
    #gets invites from the reciever side
    @staticmethod
    def get_invites(username):
        return Party_Invite.objects.get_queryset().filter(invited=Users.objects.get(username=username))

    #gets invites from the sender side
    @staticmethod
    def get_sent_invites(username):
        return Party_Invite.objects.get_queryset().filter(inviter=Users.objects.get(username=username))

    @staticmethod
    def delete_invite(sender, sent_user):
        invite = Party_Invite.objects.get(inviter=sender, invited=sent_user)
        invite.delete()


    #deletes all invites related to a user
    @staticmethod
    def delete_related_invites(user):
        invites = Party_Invite.get_sent_invites(user.username)

        for invite in invites:
            invite.delete()

class Party_Member(models.Model):
    user = models.ForeignKey(Users, blank=True, null=True, on_delete=models.CASCADE, related_name='party_member')
    in_party = models.BooleanField(blank=True, null=True, default=True)

    def __str__(self):
        return self.user.username


class Party(models.Model):
    name = models.CharField(max_length=50)
    party_leader = models.ForeignKey(Party_Member, blank=True, null=True, on_delete=models.CASCADE, related_name='party_leader')
    users = models.ManyToManyField(Party_Member, blank=True)
    invites = models.ManyToManyField(Party_Invite, blank=True)

    def __str__(self):
        return self.name

    def is_party_leader(self, user):
        return self.party_leader.user == user

    def is_member(self, user):
        for member in self.users.get_queryset():
            if member.user == user:
                return True
        return False

    #if the user is a member, deletes the member
    #if the user is a leader, replaces the leader or deletes the party
    def remove_and_rearrange(self, user):
        #checks if user is leader
        if self.is_party_leader(user):
            #gets list of all users
            user_list = list(self.users.get_queryset())
            #checks if there are any users
            if len(user_list) > 0:
                #picks next leader to be first user
                next_leader = user_list[0]
                #gets user object of the previous leader
                previous_leader = Users.objects.get(username=self.party_leader)
                #sets a new leader
                self.party_leader = next_leader
                #removes new leader from users list and deletes object associated with
                #old leader
                self.users.remove(next_leader)
                self.delete_member(previous_leader)
                self.save()
            else:
                #deletes all invites related to a party
                Party_Invite.delete_related_invites(user)

                #if there are no users the leader object and the party is deleted
                self.delete_member(user)
                self.delete()
        else:
            #if the user is not a leader, it removes the user from the users list and deletes the object
            #associated
            self.users.remove(user)
            self.delete_member(user)
            self.save()

    #Makes the model that holds the member store that the user is not in the party
    def pseudoremove_member(self, user):
        deleted_member = Party_Member.objects.get(user=user)
        deleted_member.in_party = False
        deleted_member.save()

    #completely deletes the party_member object associated with a user
    def delete_member(self, user):
        party_member = Party_Member.objects.get(user=user)
        party_member.delete()

    #gets party of a user
    @staticmethod
    def get_current_party(user):
        #searches for members and party leaders
        search_for_member = Party.objects.all().filter(users__user__username=user.username)
        search_for_leader = Party.objects.all().filter(party_leader__user=user)
        
        #returns either one or none if the current user is not in a party
        if search_for_member:
            return search_for_member.get()
        
        if search_for_leader:
            return search_for_leader.get()

        return None