from .models import Party, Party_Invite

def user_party_info(request, context):
    if request.user.is_authenticated:
        context['invites'] = Party_Invite.get_invites(username=request.user.username)