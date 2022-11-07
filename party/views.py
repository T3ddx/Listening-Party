from django.shortcuts import render
from home.views import handling_friends
# Create your views here.

def party_view(request, party_name=None):
    context = {'party_name' : party_name}
    handling_friends(request, context)
    return render(request, "party_template.html", context)