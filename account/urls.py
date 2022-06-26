from django.urls import path, include
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import csrf_protect

urlpatterns = [
    path('login/', csrf_protect(obtain_auth_token)),
    path('register/', RegisterView.as_view()),
    path('logout/', Logout.as_view()),
    path('changepassword/', ChangePasswordView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls')),

    path('wallet/', WalletDetailView.as_view()),
    path('referral/', ReferralView.as_view()),
    path('deposit/', DepositView.as_view()),
    path('withdrawal/', WithdrawalView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('trade/', TradeView.as_view()),
    path('transactions/', TransactionsView.as_view()),
]
# /api/
