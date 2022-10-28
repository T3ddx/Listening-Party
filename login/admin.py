from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UsersCreationForm, UsersChangeForm
from .models import Users, FriendProfile, FriendRequest
# Register your models here.

class UsersAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = Users
    list_display = ['email', 'username']

class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendRequest

    list_display = ["to_request", "from_request"]

class FriendsInline(admin.TabularInline):
    model = FriendProfile.friends.through

class RequestsInline(admin.TabularInline):
    model = FriendProfile.friend_requests.through

class FriendProfileAdmin(admin.ModelAdmin):
    model = FriendProfile

    inlines = [
        FriendsInline,
        RequestsInline
    ]

    list_display = ["user"]

admin.site.register(Users, UsersAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(FriendProfile, FriendProfileAdmin)