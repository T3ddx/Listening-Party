from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import spotipy.oauth2 as oauth2
from spotipy.cache_handler import CacheFileHandler
from .functions import friend_profile, handling_friends
from party.functions import user_invite_info

cid = '7f38ef08e82a41f793d5438b9910bf1d'
secret = '7cf5464267914ed9aeaca934810079dc'
redirect_uri = 'http://127.0.0.1:8000/'
scopes = 'user-read-playback-state app-remote-control user-modify-playback-state playlist-read-private user-follow-modify user-read-currently-playing user-read-playback-position playlist-modify-private playlist-modify-public user-read-email streaming user-read-private user-library-read'

# Create your views here.
def home_view(request):
    context = {}

    #gets user information regarding party invites and friends
    user_invite_info(request, context)
    friend_profile(request, context)

    if request.method == 'GET':
        if request.GET.get('code'):
            #authorizes a user to use Spotify
            auth_manager = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, scope=scopes, redirect_uri=redirect_uri, cache_handler=CacheFileHandler(username=request.user.username))
            auth_manager.get_access_token(request.GET.get('code'))
            return redirect('/')
        context['in_friends'] = False
        return render(request, 'home_template.html', context)
    else:
        handling_friends(request, context)
        return render(request, 'home_template.html', context)

