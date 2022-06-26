from datetime import timedelta
from django.utils.timezone import now
from django.conf import settings
from django.dispatch import receiver
from django.forms import ImageField
from django.urls import reverse
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create your models here.
from django.db import models
import secrets

expiration = now() + timedelta(hours=10)
class ReferralCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=154, unique=True)

    def generate_code(self):
        username = self.user.username
        x = username.split("@")
        y=x[:1]
        z=" ".join(y)
        random_code = secrets.token_hex(2)
        return z+random_code

    def save(self, *args, **kwargs):
        self.code = self.generate_code()

        return super(ReferralCode, self).save(*args, **kwargs)


class Referral(models.Model):
    referred_by = models.ForeignKey(User, unique=False, on_delete=models.DO_NOTHING, related_query_name='my_referral')
    referred_to = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_query_name='has_referred')


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    credits = models.FloatField(default=0.0)
    def __str__(self):
        return self.user.email

@ receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}, here is your password reset token: {} Copy and past in your app".format(
        reset_password_token.user.username, reset_password_token.key,)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
        fail_silently=False
    )

class Deposit(models.Model):
    user = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    deposit = models.FloatField(default=0.0)
    txid = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.txid
    
@ receiver(post_save, sender=Deposit)
def create_deposit(sender, instance, *args, **kwargs):
    if instance:
       if instance: user_obj = Wallet.objects.get(id=instance.user.id) 
    new= user_obj.credits + instance.deposit
    user_obj.credits= new
    user_obj.save()


class Withdrawal(models.Model):
    user = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    withdrawal = models.FloatField(default=0.0)
    txid = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.txid
    
@ receiver(post_save, sender=Withdrawal)
def create_withdrawal(sender, instance, *args, **kwargs):
    if instance: user_obj = Wallet.objects.get(id=instance.user.id) 
    new= user_obj.credits - instance.withdrawal
    user_obj.credits= new
    user_obj.save()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None )
    phonenumber = models.CharField(max_length=20,blank=True)
    firstname = models.CharField(max_length=500,blank=True)
    lastname = models.CharField(max_length=500,blank=True)
    dob = models.CharField(max_length=500,blank=True)
    home = models.CharField(max_length=500,blank=True)
    fax = models.CharField(max_length=500,blank=True)
    address = models.CharField(max_length=500,blank=True)
    idnumber = models.CharField(max_length=500,blank=True)
    idcardtype = models.CharField(max_length=500,blank=True)
    idfront = models.ImageField(blank=True)
    idback = models.ImageField(blank=True)
    profilepix = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class Trade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tradingpair = models.CharField(max_length=500)
    amount = models.FloatField(default=0.0)
    expires_in = models.DateTimeField(default=expiration)
    timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.tradingpair
     
@ receiver(post_save, sender=Trade)
def create_profit(sender, instance, created, **kwargs):
    if instance:
        user_obj = Wallet.objects.get(user=instance.user)  
        new = user_obj.credits + (instance.amount *1.12/100)
        user_obj.credits= new
        user_obj.save()
   
class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    txmode = models.CharField(max_length=500)
    txid = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.txmode