from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, email, **extra_fields):

        user = self.create_user(email, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user


class UserModel(AbstractBaseUser, PermissionsMixin):

    #  "email": "testuser@gmail.com",
    #  "email_verified": "true",
    #  "name" : "Test User",
    #  "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
    #  "given_name": "Test",
    #  "family_name": "User",
    #  "locale": "en"

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    picture = models.URLField(default=None, blank=True, null=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()


class Trip(models.Model):

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='organizer'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    additional_info = models.TextField(null=True)
    extra_people = models.ManyToManyField('UserModel', related_name='member', null=True)
    start_lat = models.DecimalField(max_digits=15, decimal_places=6)
    start_lon = models.DecimalField(max_digits=15, decimal_places=6)
    end_lat = models.DecimalField(max_digits=15, decimal_places=6)
    end_lon = models.DecimalField(max_digits=15, decimal_places=6)
    start_name = models.CharField(max_length=255)
    dest_name = models.CharField(max_length=255)
    votes = models.IntegerField()
