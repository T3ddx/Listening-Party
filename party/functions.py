from .models import Party, Party_Invite

def user_party_info(request, context):
    if request.user.is_authenticated:
        context['invites'] = Party_Invite.get_invites(username=request.user.username)

def create_party(request, party_name):
    party = Party.objects.create(name=party_name)
    party.users.add(request.user)