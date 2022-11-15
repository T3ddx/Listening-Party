from django.shortcuts import render
from home.functions import handling_friends, friend_profile
from .models import Party, Party_Invite
from .functions import user_party_info, create_party
# Create your views here.

def party_view(request, party_name=None):
    if request.method == 'GET':
        party_name_cleaned = party_name.replace('-', ' ')
        context = {
            'cleaned_party_name' : party_name_cleaned,
            'party_name' : party_name
        }
        friend_profile(request, context)
        handling_friends(request, context)
        user_party_info(request,context)
        create_party(request, party_name)
    return render(request, "party_template.html", context)
