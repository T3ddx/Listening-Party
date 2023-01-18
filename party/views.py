from django.shortcuts import render,redirect
from home.functions import handling_friends, friend_profile
from .models import Party, Party_Invite, Party_Member
from login.models import Users
from .functions import user_invite_info, create_party, party_info
# Create your views here.

#creates party using POST request so only invited user can use the party later
def party_validator_view(request):
    if request.method == 'POST':
        party_name = request.POST.get('party_name')

        #creates party and sets current user to party leader
        create_party(request, party_name)

        return redirect('/p/' + party_name)


def party_view(request, party_name=None):
    #returns error page if user is not logged in
    if request.user.is_authenticated:
        #checks if party is a thing, use this to verify if they weren't just playing with URL
        try:
            party = Party.objects.get(name=party_name)
        except:
            return render(request, 'error.html', {"no_party" : True})

        #if the user accessing is a leader
        if party.is_party_leader(request.user):
            #creates a party name with spaces
            party_name_cleaned = party_name.replace('-', ' ')

            #creates context
            context = {
                'cleaned_party_name' : party_name_cleaned,
                'party_name' : party_name,
                'in_party' : True
            }

            #gets friend information for user
            friend_profile(request, context)
            #handles changes of friends on this change
            handling_friends(request, context)

            #gets party info of user
            user_invite_info(request,context)
            party_info(request, context)

            if request.method == 'POST':
                handling_parties(request, context)
                
            return render(request, 'party_template.html', context)
        #if the user accessing is a member
        elif party.is_member(request.user):
            #creates a party name with spaces
            party_name_cleaned = party_name.replace('-', ' ')

            #creates context
            context = {
                'cleaned_party_name' : party_name_cleaned,
                'party_name' : party_name,
                'in_party' : True
            }

            #gets friend information for user
            friend_profile(request, context)
            #handles changes of friends on this change
            handling_friends(request, context)

            #gets party info of user
            user_invite_info(request,context)
            party_info(request, context)

            #if request.method == 'POST':
                #handling_parties(request, context)

            return render(request, 'party_template.html', context)
        return render(request, 'error.html', {'not_in_party' : True})
    return render(request, 'error.html', {'not_logged_in' : True})

def party_leader_function(request, context):
    pass

#handles the POST requests
def handling_parties(request, context):
    if request.POST.get('party_invite'):
        inviting_friends(request, context)
    if request.POST.get('delete_member'):
        remove_member(request, context)
    if request.POST.get('delete_invite'):
        remove_invite(request, context)
    
#invites a user to the party
def inviting_friends(request, context):
    invited_username = request.POST.get('party_invite')
    #checks if the username is associated with a user
    try:
        invited_user = Users.objects.get(username=invited_username)
    except:
        context['no_user'] = True
        return

    #creates a party invite object
    party_member_profile = Party_Invite.objects.create(party_name=context['party_name'], invited=invited_user, inviter=request.user)
    party_member_profile.save()

#removes a member from a party
def remove_member(request, context):
    pass

#removes an invite from a party
def remove_invite(request, context):
    context['in_party_menu'] = True
    
    invited_user = Users.objects.get(username=request.POST.get('delete_invite'))

    Party_Invite.delete_invite(request.user, invited_user)

