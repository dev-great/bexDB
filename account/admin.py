from django.contrib import admin
from .models import Escrow, NotificationPost, OTPVerification, ReferralCode, Referral, Wallet, Deposit, Withdrawal, Profile, Trade, Transactions
# Register your models here.
class ReferralCodeAdmin(admin. ModelAdmin):
    list_display = ("user", "code")
    list_filter = ("user", "code")
    search_fields = ("user", "code")

admin.site.register(ReferralCode, ReferralCodeAdmin)

class ReferralAdmin(admin. ModelAdmin):
    list_display = ("referred_by", "referred_to")
    list_filter = ("referred_by", "referred_to")
    search_fields = ("referred_by", "referred_to")

admin.site.register(Referral, ReferralAdmin) 


admin.site.register(Wallet)

class DepositAdmin(admin. ModelAdmin):
    list_display = ("user", "deposit", "txid","timestamp")
    list_filter = ("user", "deposit", "txid","timestamp")
    search_fields = ("user", "deposit", "txid","timestamp")

admin.site.register(Deposit, DepositAdmin)

class WithdrawalAdmin(admin. ModelAdmin):
    list_display = ("user", "withdrawal", "txid","timestamp")
    list_filter = ("user", "withdrawal", "txid","timestamp")
    search_fields = ("user", "withdrawal", "txid","timestamp")

admin.site.register(Withdrawal, WithdrawalAdmin)

class ProfileAdmin(admin. ModelAdmin):
    list_display = ("user", "phonenumber", "firstname", "lastname","idnumber")
    list_filter = ("user", "phonenumber", "firstname", "lastname","idnumber")
    search_fields = ("user", "phonenumber", "firstname", "lastname","idnumber")

admin.site.register(Profile, ProfileAdmin)

class TradeAdmin(admin. ModelAdmin):
    list_display = ("user", "tradingpair", "timestamp","expires_in", "active")
    list_filter = ("user", "tradingpair","timestamp", "expires_in", "active")
    search_fields = ("user", "tradingpair","timestamp", "expires_in", "active")

admin.site.register(Trade, TradeAdmin)

class TransactionsAdmin(admin. ModelAdmin):
    list_display = ("user", "txmode", "amount", "txid","timestamp","status")
    list_filter = ("user", "txmode", "amount","txid","timestamp","status")
    search_fields = ("user", "txmode","amount", "txid","timestamp","status")

admin.site.register(Transactions, TransactionsAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', ]
    list_per_number = 50
    list_filter = ['title', 'date', ]
    search_fields = ['title', 'date']


admin.site.register(NotificationPost, NotificationAdmin)

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ['user','phonenumber', 'isVerified', 'timestamp']
    list_per_number = 50
    list_filter = ['user','phonenumber',]
    search_fields = ['user','phonenumber',]


admin.site.register(OTPVerification, OTPVerificationAdmin)



class EscrowAdmin(admin. ModelAdmin):
    list_display = ("user", "transactype", "amount", "qnt","cointobuy","paymentmethod", "receivingmethod")
    list_filter = ("user", "transactype", "amount", "qnt","cointobuy","paymentmethod", "receivingmethod")
    search_fields = ("user", "transactype", "amount", "qnt","cointobuy","paymentmethod", "receivingmethod")

admin.site.register(Escrow, EscrowAdmin)