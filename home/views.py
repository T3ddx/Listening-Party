import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import spotipy.oauth2 as oauth2
from spotipy.cache_handler import CacheFileHandler
from login.models import FriendProfile, FriendRequest, Users

cid = '7f38ef08e82a41f793d5438b9910bf1d'
secret = '7cf5464267914ed9aeaca934810079dc'
redirect_uri = 'http://127.0.0.1:8000/'
scopes = 'user-read-playback-state app-remote-control user-modify-playback-state playlist-read-private user-follow-modify user-read-currently-playing user-read-playback-position playlist-modify-private playlist-modify-public user-read-email streaming user-read-private user-library-read'

# Create your views here.

def home_view(request):
    context = {}
    if request.method == 'GET':
        if request.GET.get('code'):
            #authorizes a user to use Spotify
            auth_manager = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, scope=scopes, redirect_uri=redirect_uri, cache_handler=CacheFileHandler(username=request.user.username))
            auth_manager.get_access_token(request.GET.get('code'))
            return redirect('/')
        if request.user.is_authenticated:
            #adds a users friend profile to the context to be used in the template
            context["FriendProfile"] = FriendProfile.objects.get(user=request.user)
        context['in_friends'] = False
        return render(request, 'home_template.html', context)
    else:
        if request.user.is_authenticated:
            context["FriendProfile"] = FriendProfile.objects.get(user=request.user)
        context['in_friends'] = True
        if request.POST.get('accept'):
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
            context['in_friends'] = 'initial'
        elif request.POST.get('cancel'):
            #cancels a friend request
            canceling = FriendRequest.objects.get(to_request=Users.objects.get(username=request.POST.get('cancel')), from_request=request.user)
            canceling.delete()
        elif request.POST.get('send_request'):
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
                    return render(request, 'home_template.html', context)

                already_sent_request = from_profile.friend_requests.get_queryset().filter(from_request=from_user, to_request=to_user)
                if already_sent_request.count() != 0:
                    context['already_sent_request'] = True
                    return render(request, 'home_template.html', context)

                friend_request = FriendRequest.objects.create(to_request=to_user, from_request=from_user)
                
                to_profile.friend_requests.add(friend_request)
                from_profile.friend_requests.add(friend_request)

                friend_request.save()
                to_profile.save()
                from_profile.save()
            except ObjectDoesNotExist:
                context["cant_find_user"] = True
        elif request.POST.get('delete'):
            #deletes a friend from a user's friend profile
            del_user = Users.objects.get(username=request.POST.get('delete'))
            curr_user = request.user
            del_user_profile = FriendProfile.objects.get(user=del_user)
            curr_user_profile = FriendProfile.objects.get(user=curr_user)

            del_user_profile.friends.remove(curr_user)
            curr_user_profile.friends.remove(del_user)

            del_user_profile.save()
            curr_user_profile.save()
        return render(request, 'home_template.html', context)