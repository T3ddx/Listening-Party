from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#user model
class Users(AbstractUser):

    def __str__(self):
        return self.username

#friend request model
class FriendRequest(models.Model):
    to_request = models.ForeignKey(Users, related_name='to_request', on_delete=models.CASCADE)
    from_request = models.ForeignKey(Users, related_name='from_request', on_delete=models.CASCADE)

    def __str__(self):
        return self.from_request.username + " to " + self.to_request.username

#friend profile model
#contains user, friend requests and friends
class FriendProfile(models.Model):
    user = models.OneToOneField(Users, related_name='user', on_delete=models.CASCADE)
    friends = models.ManyToManyField(Users, blank=True)
    friend_requests = models.ManyToManyField(FriendRequest, blank=True)

    def __str__(self):
        return self.user.username
    
    def get_to_requests(self):
        return self.friend_requests.get_queryset().filter(to_request=self.user)

    def get_sent_requests(self):
        return self.friend_requests.get_queryset().filter(from_request=self.user)
