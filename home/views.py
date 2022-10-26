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
        if request.POST.get('accept'):
            #adds a friend to two users friend profiles and deletes the friend request
            #and tells the template that the user is accessing the friends interface
            context['in_friends'] = True
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
            context['in_friends'] = True
            #deletes a friend request
            canceling = FriendRequest.objects.get(to_request=Users.objects.get(username=request.POST.get('cancel')), from_request=request.user)
            canceling.delete()
        elif request.POST.get('send_request'):
            context['in_friends'] = True
            try:
                user = Users.objects.get(username=request.POST.get('send_request'))
            except ObjectDoesNotExist:
                context["cant_find_user"] = True
        if request.user.is_authenticated:
            context["FriendProfile"] = FriendProfile.objects.get(user=request.user)
        return render(request, 'home_template.html', context)