import base64
from django.shortcuts import render
import pyotp
from .models import *
from .serializers import *
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token

class RegisterView(APIView):
    csrf_protect_method = method_decorator(csrf_protect)

    def post(self, request):
        serializers = UserSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response( serializers.data, status=200)
        return Response( serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token":token.key}, status=201)


class WalletDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data, status=200)


class ReferralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        code = ReferralCode.objects.get(user=request.user)
        serializer = ReferralCodeSerializer(code)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = ReferralCodeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionsView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        serializers = Transactionsserializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=user)
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return Transactionsserializer

    def get(self, request):

        username = request.user.username
        user = User.objects.get(username__exact=username)
        detail = user.username

        transactions = Transactions.objects.filter(user=user)
        serializer = Transactionsserializer(transactions, many=True)
        return Response(serializer.data)


class TradeView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        serializers = Tradeserializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=user)
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



    def get_serializer_class(self):
        return Tradeserializer

    def get(self, request):

        username = request.user.username
        user = User.objects.get(username__exact=username)
        detail = user.username

        trade = Trade.objects.filter(user=user)
        serializer = Tradeserializer(trade, many=True)
        return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)
    

    def patch(self, request):
        username = request.user
        profile = Profile.objects.get(user__exact=username)

        serializers = Profileserializer(
            profile, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get_serializer_class(self):
        return Profileserializer

    def get(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        profile = Profile.objects.filter(user=user)
        serializer = Profileserializer(profile, many=True)
        return Response(serializer.data)


class WithdrawalView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return Withdrawalserializer

    def get(self, request):
        username = request.user
        user = Wallet.objects.get(user__exact=username)
        withdrawal = Withdrawal.objects.filter(user=user)
        serializer = Withdrawalserializer(withdrawal, many=True)
        return Response(serializer.data)

class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return Depositserializer

    def get(self, request):
        username = request.user
        user = Wallet.objects.get(user__exact=username)
        deposit = Deposit.objects.filter(user=user)
        serializer = Depositserializer(deposit, many=True)
        return Response(serializer.data)

class NotificationView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        start_date = user.date_joined

        notifications = NotificationPost.objects.filter(date__gte=start_date)
        serializer = Notificationserializer(notifications, many = True)
        return Response(serializer.data)


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    
    @staticmethod
    def get(request, phone):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        user_email = user.email
        user_nameF = user.first_name
        user_nameL = user.last_name
        try:
            phonenumber = OTPVerification.objects.get(phonenumber=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            OTPVerification.objects.create(
                phonenumber=phone,
            )
            phonenumber = OTPVerification.objects.get(phonenumber=phone)  # user Newly created Model
        phonenumber.counter += 1  # Update Counter At every Call
        phonenumber.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(phonenumber.counter))
        msg = f'DO NOT DISCLOSE. Dear {user_nameF} {user_nameL}, The OTP for your confirmation is : {OTP.at(phonenumber.counter)} to verify {phonenumber}. Thank you for choosing BEX.'
        send_mail('BEX OTP Withdrawal Verification', msg, settings.EMAIL_HOST_USER,
        [user_email], fail_silently=False)
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(phonenumber.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            phonenumber = OTPVerification.objects.get(phonenumber=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  
        if OTP.verify(request.data["otp"], phonenumber.counter):  # Verifying the OTP
            phonenumber.isVerified = True
            phonenumber.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)

class OTPView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        serializers = OTPserializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=user)
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

  
class EscrowView(APIView):
    permission_classes = [IsAuthenticated]
    csrf_protect_method = method_decorator(csrf_protect)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username__exact=username)
        serializers = Escrowserializer(data=request.data)
        if serializers.is_valid():
            serializers.save(user=user)
            return Response({"error": False})
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return Escrowserializer

    def get(self, request):

        username = request.user.username
        user = User.objects.get(username__exact=username)
        detail = user.username

        escrow = Escrow.objects.filter(user=user)
        serializer = Escrowserializer(escrow, many=True)
        return Response(serializer.data)

 