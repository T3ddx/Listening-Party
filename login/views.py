from .forms import UsersCreationForm, UsersChangeForm
from .models import Users, FriendProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import spotipy.oauth2 as oauth2
from spotipy.cache_handler import CacheFileHandler

cid = '7f38ef08e82a41f793d5438b9910bf1d'
secret = '7cf5464267914ed9aeaca934810079dc'
redirect_uri = 'http://127.0.0.1:8000/'
scopes = 'user-read-playback-state app-remote-control user-modify-playback-state playlist-read-private user-follow-modify user-read-currently-playing user-read-playback-position playlist-modify-private playlist-modify-public user-read-email streaming user-read-private user-library-read'

# Create your views here.

#logs a user in
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            #logs user in if they exist
            user.logged_in = True
            user.save()
            login(request, user)
            return redirect('/')
        else:
            #sends an error if the user doesn't exist
            context = {
                'error' : 'Incorrect Username or Password'
            }
            return render(request, 'accounts/login_template.html', context)
    return render(request, 'accounts/login_template.html', {})

#logs a user out
def logout_view(request):
    if request.method == 'POST':
        request.user.logged_in = False
        logout(request)
        return redirect('/')
    return render(request, 'accounts/logout_template.html', {})

#signs a user up using the UsersCreationForm
def signup_view(request):
    form = UsersCreationForm(request.POST or None)
    context = {
        'form' : form
    }
    if form.is_valid():
        #creates a friend profile for the user and saves them
        user_obj = form.save()
        profile = FriendProfile.objects.create(user=user_obj)
        profile.save()
        login(request, user_obj)
        user_obj.logged_in = True
        #sents user to be authenticated on Spotify
        auth_manager = oauth2.SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redirect_uri, scope=scopes)

        redirect_url = auth_manager.get_authorize_url()
        return redirect(redirect_url)
    return render(request, 'accounts/signup_template.html', context)
