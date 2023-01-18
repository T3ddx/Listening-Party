from django.shortcuts import render, HttpResponse

from party.models import Party, Party_Invite, Party_Member
from .functions import invite_html
# Create your views here.

def get_party_info(request):
    html = ''

    print(request.GET.get('party'))

    if request.GET.get('party'):
        html = 'lol'
    else:
        html = "Create a Party:\n<form id='party_form' method='post' action='/p/'>\n{% csrf_token %}\n<input type='text' id='party_name' name='party_name' placeholder='enter party name' autocomplete='off'>\n<button id='input_button' type='submit'>+</button>\n</form>\n<p1 id='party_sym_error' class='error_message' style='display:none;'>Not a valid party name. Cannot include these symbols: </p1>\n<p1 id='party_len_error' class='error_message' style='display:none;'>Party name must not be over 50 characters.</p1>"

    html = invite_html(request.user, html)
        
    return HttpResponse(html)