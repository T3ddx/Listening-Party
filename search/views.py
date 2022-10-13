from http import server
from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Create your views here.

cid = '7f38ef08e82a41f793d5438b9910bf1d'
secret = '7cf5464267914ed9aeaca934810079dc'

def search_view(request):
    oauth_object = spotipy.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri='http://127.0.0.1:8000/')
    token_dict = oauth_object.get_access_token()
    token =token_dict['access_token']
    sp = spotipy.Spotify(auth=token)
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



    