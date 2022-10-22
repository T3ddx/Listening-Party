from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    def __str__(self):
        return self.username

class FriendRequest(models.Model):
    to_request = models.OneToOneField(Users, related_name='to_request', on_delete=models.CASCADE)
    from_request = models.OneToOneField(Users, related_name='from_request', on_delete=models.CASCADE)

class FriendProfile(models.Model):
    user = models.OneToOneField(Users, related_name='user', on_delete=models.CASCADE)
    friends = models.ManyToManyField(Users, blank=True)
    friend_requests = models.ForeignKey(FriendRequest, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_friend_request(self):
        if self.friend_requests:
            return (self.friend_requests.to_request.username, self.friend_requests.from_request.username)
        else:
            return "No Friend Requests"