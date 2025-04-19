
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Profile, AccountUser
from core.models import Wallets, Transaction
 
from django.core.mail import send_mail

 
User = settings.AUTH_USER_MODEL
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        
        Profile.objects.create(user=instance)
        Wallets.objects.create(user=instance) 
        
        print('[SIGNALS] Created Profile, Wallet and Transaction models')
        print("New user profile has been created for ", instance.email)
        # send email to new user
        #send_mail( subject, message, email_from, recipient_list )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.wallets.save()
    print("Profile saved!")
   
 

