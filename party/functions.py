from .models import Party, Party_Invite, Party_Member

#gets invites of party
def user_invite_info(request, context):
    if request.user.is_authenticated:
        context['invites'] = Party_Invite.get_invites(username=request.user.username)

#adds party info to context
def party_info(request, context):
    party = Party.objects.get(party_leader__user=request.user)
    context['party_members'] = party.users.all()
    context['invited_members'] = Party_Invite.get_sent_invites(request.user.username)

#adds party leader to context and creates the party object
def create_party(request, party_name):
    party_leader = Party_Member.objects.create(user=request.user)

    party = Party.objects.create(name=party_name, party_leader=party_leader)

    party_leader.save()
    party.save()
    

