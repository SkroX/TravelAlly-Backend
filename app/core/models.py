from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
