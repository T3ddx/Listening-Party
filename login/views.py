from .forms import UsersCreationForm, UsersChangeForm
from .models import Users
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/')
        else:
            context = {
                'error' : 'Incorrect Username or Password'
            }
            return render(request, 'accounts/login_template.html', context)
    return render(request, 'accounts/login_template.html', {})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'accounts/logout_template.html', {})

def signup_view(request):
    user = Users.objects.get(email='teddy.dumitru@yahoo.com')
    print("user token: " + user.token)
    '''
    form = UsersCreationForm(request.POST or None)
    context = {
        'form' : form
    }
    #if form.is_valid():
        #user_obj = form.save()
        #user_obj.get["token"]
    '''
    return render(request, 'accounts/signup_template.html', {})
