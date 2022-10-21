from http import server
from django.shortcuts import render
import spotipy
from spotipy import oauth2
from spotipy.cache_handler import CacheHandler,CacheFileHandler

# Create your views here.

cid = '7f38ef08e82a41f793d5438b9910bf1d'
secret = '7cf5464267914ed9aeaca934810079dc'
redirect_uri = 'http://127.0.0.1:8000/'
scopes = 'user-read-playback-state app-remote-control user-modify-playback-state playlist-read-private user-follow-modify user-read-currently-playing user-read-playback-position playlist-modify-private playlist-modify-public user-read-email streaming user-read-private user-library-read'

def search_view(request):
    auth_manager = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, scope=scopes, redirect_uri=redirect_uri, cache_handler=CacheFileHandler(username=request.user.username))
    sp = spotipy.Spotify(auth_manager=auth_manager)
    query = request.GET.get('query')

    if query != '':
        query.replace(' ', '%20')
        results = sp.search(q=query, limit=10, type='track,artist')
        context = {
            'songs': results['tracks']['items'],
        }
        print(results['tracks']['items'][0])
        sp.start_playback(uris=['spotify:track:0ypjMI7vHiDP4sLB1C0Qna'])
        return render(request, 'search_template.html', context=context)
    
    return render(request, 'search_template.html')



    