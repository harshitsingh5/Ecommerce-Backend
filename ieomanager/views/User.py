from rest_framework import generics,mixins
from rest_framework.views import APIView
from ieomanager.Serializers.UserSerializer import UserSerializer
from ieomanager.models import User
from ieomanager.repository import UserRepository
from ieomanager.utilities import auth_login_required
from rest_framework.response import Response

class UserCLSOperations(generics.ListCreateAPIView):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	
	def post(self,request,*args,**kwargs):
		return self.create(request,*args,**kwargs)

class UserRUDOperations(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	lookup_field  = 'uuid'

	queryset = User.objects.all()

	def get_queryset(self):
		return self.queryset


class Users_filtered(APIView):
	br=UserRepository()

	#view filtered Users for Admin
	@auth_login_required(['admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			users=self.br.GetAll()
		else:
			users = self.br.GetAll(filters=[('status',status)])
		data = UserSerializer(users, many=True).data
		return Response(data)
