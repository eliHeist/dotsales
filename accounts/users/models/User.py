from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Group,
)
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


# Create your models here.
class UserManager(BaseUserManager):
    """Class to manage the creation of user objects"""

    def create_user(self, email, password, username=None, **extra_fields):
        """Creates and returns a user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Optionals:
        is_staff: Boolean to indicate a user is staff or not
        is_admin: Boolean to indicate a user is an admin or not
        is_active: Boolean to indicate a user can login or not

        Return:
            A user object
        """

        if not email:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(username=username, email = self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        """Creates an admin user object
        Arguments:
        username: the string to use as username
        email: the string to use as email
        password: the string to use as password

        Return:
            A user object
        """
        user = self.create_user(email, password=password, username=username)
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    accessible_branches = models.ManyToManyField("companies.Branch", blank=True, related_name="users_with_access")

    is_company_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def deactivate(self, using=None, keep_parents=False):
        self.is_active ^= True
        self.save()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin