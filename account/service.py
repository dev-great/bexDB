from .models import Referral, Wallet
import os

class CreateReferral():
    def __init__(self, referred_by, referred_to):
        self.referred_by = referred_by
        self.referred_to = referred_to

    def new_referral(self):
        Referral.objects.create(referred_by=self.referred_by, referred_to=self.referred_to)


class SendReferral():
    register_page = 'abc@abc.com'

    def __init__(self, mail_id, referral_code):
        self.mail_id = mail_id
        self.referral_code = referral_code


