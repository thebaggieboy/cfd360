from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from .choices import *
from django.contrib.postgres.fields import ArrayField

User = settings.AUTH_USER_MODEL
 
import uuid

CRYPTOCURRENCY_CHOICES = (
    ("Ask live chat for your address", "Ask live chat for your address"),
    ("Bitcoin", "Bitcoin"),
    ("Ethereum", "Ethereum"),
    ("USDC", "USDC")
)


CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)
STATUS = (
	('Pending', 'Pending'), 
	('Completed', 'Completed')
)
VERIFICATION_STATUS = (
	('Pending', 'Pending'), 
	('Verified', 'Verified')
)

WITHDRAW_CHOICE = (
	('Bank', 'Bank'), 
	('Bitcoin', 'Bitcoin')
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class AccountUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
   
    first_name = models.CharField(max_length=250, default='',null=True, blank=True)
    last_name = models.CharField(max_length=250, default='' ,null=True, blank=True)
    mobile_number = models.CharField(max_length=250, default='', null=True, blank=True)
    country = models.CharField(max_length=250, default='', null=True, blank=True)  
     
    billing_address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.CharField(max_length=250, default='')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email


    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

 


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
     
    amount = models.CharField(max_length=250, null=True, blank=True, default=0.0)
    payment_method = models.CharField(max_length=250, null=True, blank=True, choices=WITHDRAW_CHOICE, default='Bitcoin')
    slug = models.SlugField(max_length=250,blank=True, null=True)
    verification_status = models.CharField(choices=VERIFICATION_STATUS, default='Pending', max_length=250, null=True, blank=True,)
    

    date_created = models.DateTimeField(max_length=250, null=True, blank=True, default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.email)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("core:profile", kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.user} profile'

 
 