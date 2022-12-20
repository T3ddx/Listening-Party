from .models import Party, Party_Invite

#gets invites of party
def user_invite_info(request, context):
    if request.user.is_authenticated:
        context['invites'] = Party_Invite.get_invites(username=request.user.username)

#adds party info to context
def party_info(request, context):
    party = Party.objects.get(party_leader=request.user)
    context['party_members'] = party.users.all()
    context['invited_members'] = Party_Invite.get_party_invites(request.user.username)

#adds party leader to context and creates the party object
def create_party(request, party_name):
    party = Party.objects.create(name=party_name, party_leader=request.user)
    party.save()
    

