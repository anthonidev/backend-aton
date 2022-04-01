from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField

from .Countries import Countries
User = settings.AUTH_USER_MODEL


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprise = models.CharField(max_length=255, default='')
    photo = CloudinaryField('Image', overwrite=True, format="jpg", blank=True, null=True)
    city = models.CharField(
        max_length=255, choices=Countries.choices, default=Countries.Lima)

    address_line_1 = models.CharField(max_length=255, default='')
    address_line_2 = models.CharField(max_length=255, default='')

    district = models.CharField(max_length=255, default='')
    zipcode = models.CharField(max_length=20, default='')

    phone = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.user.first_name
