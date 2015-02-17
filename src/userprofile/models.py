from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
	user = models.OneToOneField(User)  ## One user profile associated with one user
	likes_cheese = models.BooleanField(default=True)
	favorite_cadre = models.CharField(max_length=50)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

