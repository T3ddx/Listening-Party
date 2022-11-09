from django.contrib import admin

from .models import Party, Party_Invite
# Register your models here.
class PartyInviteAdmin(admin.ModelAdmin):
    model = Party_Invite

    list_display = ['party_name', 'inviter', 'invited']

class PartyInline(admin.TabularInline):
    model = Party.users.through

class InviteInline(admin.TabularInline):
    model = Party.invites.through

class PartyAdmin(admin.ModelAdmin):
    model = Party

    inlines = [
        PartyInline,
        InviteInline
    ]

    list_display = ['name']

admin.site.register(Party, PartyAdmin)
admin.site.register(Party_Invite, PartyInviteAdmin)