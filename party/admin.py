from django.contrib import admin

from .models import Party, Party_Invite, Party_Member
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

    list_display = ['name', 'party_leader']

class Party_MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'in_party']

admin.site.register(Party, PartyAdmin)
admin.site.register(Party_Invite, PartyInviteAdmin)
admin.site.register(Party_Member, Party_MemberAdmin)