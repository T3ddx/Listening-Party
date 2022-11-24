from login.models import FriendProfile, FriendRequest, Users
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

def friend_profile(request, context):
    if request.user.is_authenticated:
        #adds a users friend profile to the context to be used in the template
        friend_profile = FriendProfile.objects.get(user=request.user)
        context["FriendProfile"] = friend_profile

def accepting_friends(request, context):
    #adds a friend to two users friend profiles and deletes the friend request
    #and tells the template that the user is accessing the friends interface
    accepting = FriendRequest.objects.get(to_request=request.user, from_request=Users.objects.get(username=request.POST.get('accept')))

    profile = FriendProfile.objects.get(user=request.user)
    profile.friends.add(accepting.from_request)
    profile.save()

    profile2 = FriendProfile.objects.get(user=accepting.from_request)
    profile2.friends.add(request.user)
    profile2.save()

    accepting.delete()
    context['in_friends'] = True

def cancel_friends(request, context):
    #cancels a friend request
    canceling = FriendRequest.objects.get(to_request=Users.objects.get(username=request.POST.get('cancel')), from_request=request.user)
    canceling.delete()
    context['in_friends'] = True

def add_friend(request, context):
    try:
        #gets the users that are related to the friend request
        #creates the friend request object
        #adds the object to the user's friend profiles
        to_user = Users.objects.get(username=request.POST.get('send_request'))
        from_user = request.user
        to_profile = FriendProfile.objects.get(user=to_user)
        from_profile = FriendProfile.objects.get(user=from_user)

        #checks if the profile already has the user as a friend or
        #sent them a friend request
        already_friends = from_profile.friends.get_queryset().filter(username=to_user.username)
        if already_friends.count() != 0:
            context['already_friends'] = True
            context['in_friends'] = True 
            return render(request, 'home_template.html', context)

        already_sent_request = from_profile.friend_requests.get_queryset().filter(from_request=from_user, to_request=to_user)
        if already_sent_request.count() != 0:
            context['already_sent_request'] = True
            context['in_friends'] = True
            return render(request, 'home_template.html', context)

        friend_request = FriendRequest.objects.create(to_request=to_user, from_request=from_user)
        
        to_profile.friend_requests.add(friend_request)
        from_profile.friend_requests.add(friend_request)

        friend_request.save()
        to_profile.save()
        from_profile.save()
    except ObjectDoesNotExist:
        context["cant_find_user"] = True
    context['in_friends'] = True

def delete_friend(request, context):
    #deletes a friend from a user's friend profile
    del_user = Users.objects.get(username=request.POST.get('delete'))
    curr_user = request.user
    del_user_profile = FriendProfile.objects.get(user=del_user)
    curr_user_profile = FriendProfile.objects.get(user=curr_user)

    del_user_profile.friends.remove(curr_user)
    curr_user_profile.friends.remove(del_user)

    del_user_profile.save()
    curr_user_profile.save()
    context['in_friends'] = True

def handling_friends(request, context):
    if request.POST.get('accept'):
        accepting_friends(request, context)
    elif request.POST.get('cancel'):
        cancel_friends(request, context)
    elif request.POST.get('send_request'):
        add_friend(request, context)
    elif request.POST.get('delete'):
        delete_friend(request, context)