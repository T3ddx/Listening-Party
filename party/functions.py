from .models import Party, Party_Invite

#gets invites of party
def user_party_info(request, context):
    if request.user.is_authenticated:
        context['invites'] = Party_Invite.get_invites(username=request.user.username)

#adds party leader to context and creates the party object
def create_party(request, party_name, context):
    context['party_leader'] = request.user.username
    party = Party.objects.create(name=party_name, party_leader=request.user)
    party.save()

    

