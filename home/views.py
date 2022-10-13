from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '76a2058c4dfa4c90a67af9a268a2581f'
secret = '4d582988167d4fd3b12f03d3f9f14742'

# Create your views here.

def home_view(request):
    return render(request, 'home_template.html')