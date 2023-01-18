from party.models import Party_Invite

def invite_html(user, html):
    invites = Party_Invite.get_invites(user)

    for invite in invites:
        html += f"<form method='post' action='p/{{ invite.party_name }}'>\n{{% csrf_token %}}\n{ invite.party_name } | { invite.inviter }<button type='submit' name='party_join' value='{ invite.party_name }' class='list_buttons'>join</button>\n</form>"

    return html