from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.fields import CurrentUserDefault
from django.db import transaction
from ieomanager.Serializers import *
from ieomanager.models import *
from ieomanager.repository import *
from django.utils import timezone
from ieomanager.permisions import IsAdminOrOwner
from functools import partial
from ieomanager.utilities import auth_login_required
import json
from rest_framework import parsers


class Admin_user_booking(APIView):
	br=BookingsRepository()
	ur = UserRepository()
	# parser_classes = (parsers.MultiPartParser,)
	#view List of particular User
	@auth_login_required(['admin'])
	def get(self,request):
		user_uuid = request.GET['user_uuid']
		user = self.ur.GetFirst(filters=[('uuid',user_uuid)])
		if not user:
			return Response({"msg":"User not found"})
		status = request.GET['status']
		bookings = self.br.GetAll(filters=[('user',user),('status',status)])
		# if request.GET.get('include'):
		# 	bookings = BookingsSerializer.setup_eager_loading(bookings)
		data = BookingsSerializer(bookings, many=True).data
		return Response(data)


class Admin_user_details(APIView):
	ur = UserRepository()
	#view List of particular User
	@auth_login_required(['admin'])
	def get(self,request):
		user_uuid = request.GET['user_uuid']
		user = self.ur.GetFirst(filters=[('uuid',user_uuid)])
		if not user:
			return Response({"msg":"User not found"})
		user_serializer=UserSerializer(user).data
		return Response(user_serializer)