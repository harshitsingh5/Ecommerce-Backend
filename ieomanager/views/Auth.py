from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ieomanager.Serializers import LoginSerializer,SignUpSerializer,OtpVerifySerializer,UserSerializer
from ieomanager.models import User,Cart_status
from ieomanager.models import User_status
from ieomanager.repository import UserRepository,OtpRepository,CartRepository
from ieomanager.utilities import JWTService,auth_login_required
from ieodev.settings import *
from random import randint
from datetime import datetime,timedelta
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
import bcrypt
import smtplib
import ssl


def email(receiver_email,subject,body):
	port = EMAIL_PORT
	smtp_server = EMAIL_HOST
	sender_email = EMAIL_HOST_USER
	password = EMAIL_HOST_PASSWORD
	# receiver_email = 'example@example.com'
	# subject = 'Website registration'
	# body = 'Activate your account.'
	message = 'Subject: {}\n\n{}'.format(subject, body)
	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
		# server.ehlo()  # Can be omitted
		server.starttls(context=context)
		# server.ehlo()  # Can be omitted
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)
		return "email sent"
	return "email sending failed"


class Login(APIView):
	permission_classes = [AllowAny]

	def post(self,request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		if not user:
			return Response({"msg":"No Such User Found"},status=400)
		jwt=JWTService()
		token=jwt.create_token(user.uuid, user.get_role())
		user_serializer=UserSerializer(user)
		return Response({"token":token,"user":user_serializer.data},status=200)

class SignUp(APIView):
	permission_classes = [AllowAny]
	repository=UserRepository()
	otp_repository=OtpRepository()
	def post(self,request):
		serializer = SignUpSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		request_data = serializer.validated_data
		user=self.repository.GetFirst(filters=[('email_id',request_data['email'])])
		if not user:
			password = str(request_data['password'])
			passwd =  bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
			user = self.repository.Create(values={'name':request_data['name'],"email_id":request_data['email'],"password":passwd,'mobile_number':request_data['mobile_number']})
		if user:
			all_otps=user.otp.all()
			for otp in all_otps:
				self.otp_repository.Destroy(otp)
				# otp.delete()
			# otp = randint(100000,999999)
			otp = 11111
			otp_obj = self.otp_repository.Create(values={"user":user,"otp":otp,"valid_till":timezone.now()+timezone.timedelta(minutes=5)})

			# EMAIL SENDING CODE
			sender_email = 'connect@xyz.com'
			receiver_email = str(user.email_id)
			subject = 'OTP from XYZ'
			body = 'Your OTP is ' + str(otp) + '. It is valid for 5 minutes.'
			x = ''
			x = email(receiver_email,subject,body)
			if x == 'email sent':
				return Response({
					"email_status": "email sent",
					"message":"An OTP has been sent to your email. Please verify Account",
					},status=200
				)
			elif x == 'email sending failed':
				return Response({
					"email_status": "email sending failed",
					"message":"An OTP has been sent to your email. Please verify Account",
					},status=200
				)


			# send_mail('OTP from XYZ',
			# 'Your OTP is ' + str(otp) + '. It is valid for 5 minutes.',
			# 'connect@xyz.com',
			# [user.email_id],
			# fail_silently=False)

			# email = EmailMessage(
			# 	subject = 'OTP from XYZ',
			# 	body = 'Your OTP is ' + str(otp) + '. It is valid for 5 minutes.',
			# 	from_email = 'from@xyz.com',
			# 	to = [user.email_id],
			# 	# bcc = ['bcc@anotherbestuser.com'],
			# 	# reply_to = ['whoever@itmaybe.com'],
			# )
			# email.send()

			return Response({
				"message":"An OTP has been sent to your email. Please verify Account",
				},status=200
			)
		else:
			return Response({"message":"cannot create user"},status=422)


class Resend_otp(APIView):
	permission_classes = [AllowAny]
	user_repository=UserRepository()
	otp_repository=OtpRepository()
	def post(self,request):
		user = self.user_repository.GetFirst(filters=[('email_id',request.data['email'])])
		if not user:
			return Response({"message":"User Not Found"}, status=404)
		otp_obj=user.otp.first()
		sender_email = 'connect@xyz.com'
		receiver_email = str(user.email_id)
		subject = 'OTP from XYZ'
		body = 'Your OTP is ' + str(otp_obj.otp) + '. It is valid for 5 minutes.'
		x = ''
		x = email(receiver_email,subject,body)
		if x == 'email sent':
			return Response({
				"email_status": "email sent",
				"message":"An OTP has been sent to your email. Please verify Account",
				},status=200
			)
		elif x == 'email sending failed':
			return Response({
				"email_status": "email sending failed",
				"message":"An OTP has been sent to your email. Please verify Account",
				},status=200
			)


class OtpVerify(APIView):
	permission_classes = [AllowAny]
	repository=OtpRepository()
	user_repository=UserRepository()
	cr=CartRepository()
	def post(self, request):
		serializer = OtpVerifySerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		request_data = serializer.validated_data
		user = self.user_repository.GetFirst(filters=[('email_id',request_data['email'])])
		if not user:
			return Response({"message":"User Not Found"}, status=404)
		# if not user.otp.first():
		#     return Response({"message":"No OTP found for user"}, status=402)
		otp_obj=user.otp.first()
		if otp_obj.otp==request_data['otp']:
			if otp_obj.valid_till>timezone.now():
				user.status='User_status.email_verified'
				user.save()
				cart = self.cr.Create(values={"user":user,"status":Cart_status.active})
				self.repository.Destroy(otp_obj)
				jwt=JWTService()
				token=jwt.create_token(user.uuid, user.get_role())
				user_serializer=UserSerializer(user)
				return Response({"token":token,"user":user_serializer.data},status=200)
			else:
				return Response({"message":"OTP Expired"}, status=422)
		else:
			return Response({"message":"Invalid OTP"}, status=422)


class Logout(APIView):
	authentication_classes = { TokenAuthentication , }
	def post(self,request):
		return Response(status=204)


class ForgotPassword1(APIView):
	permission_classes = [AllowAny]
	otp_repository=OtpRepository()
	user_repository=UserRepository()
	def post(self,request):
		email_id = request.data['email_id']
		user = self.user_repository.GetFirst(filters=[('email_id',email_id)])
		if not user:
			return Response({"message":"User Not Found"}, status=404)
		all_otps=user.otp.all()
		for otp in all_otps:
			self.otp_repository.Destroy(otp)
			# otp.delete()
		otp = '00000'
		otp_obj = self.otp_repository.Create(values={"user":user,"otp":otp,"valid_till":timezone.now()+timezone.timedelta(minutes=5)})
		otp_obj.token=otp_obj.uuid
		otp_obj.save()
		link="www.ultimateshark.in:8000/forgot-password-token/"+otp_obj.uuid
		return Response({"msg":"Password reset link sent to your email address.","link":link},status=200)


class ForgotPassword2(APIView):
	permission_classes = [AllowAny]
	otp_repository=OtpRepository()
	user_repository=UserRepository()
	def post(self,request):
		token = request.data['token']
		otp = self.otp_repository.GetFirst(filters=[('token',token)])
		if not otp:
			return Response({"message":"Reset link not found"}, status=404)
		user=otp.user
		if not user:
			return Response({"message":"User Not Found"}, status=404)
		password = str(request.data['password'])
		passwd =  bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		user.password=passwd
		user.save()
		otp.delete()
		return Response({"msg":"Password reset successful"},status=200)