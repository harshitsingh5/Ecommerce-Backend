from rest_framework.views import APIView
from rest_framework.response import Response
from ieomanager.repository import UserRepository,AdminRepository
from ieomanager.utilities import auth_login_required
from ieomanager.Serializers import CreateAdminSerializer,AdminLoginSerializer,UserSerializer, AdminSerializer
from ieomanager.models import User_status
from ieomanager.utilities import JWTService,auth_login_required
import bcrypt

class CreateAdmin(APIView):
	repository=UserRepository()
	admin_repo = AdminRepository()
	@auth_login_required(['admin'])
	def post(self,request):
		serializer = CreateAdminSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		request_data = serializer.validated_data
		password = str(request_data['password'])
		passwd =  bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
		user = self.repository.Create(values={"name":request_data['name'],"email_id":request_data['email'],"password":passwd,'mobile_number':request_data['mobile_number']})
		user.status=User_status.email_verified
		user.save()
		role=request.data['role']
		admin = self.admin_repo.Create(values={"user":user,"admin_type":role})
		return Response({"message":"Admin Created"},status=201)


class AdminLogin(APIView):
	def post(self,request):
		serializer = AdminLoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		if not user:
			return Response({"msg":"No Such User Found"},status=400)
		jwt=JWTService()
		token=jwt.create_token(user.uuid, user.get_role())
		return Response({"token":token},status=200)


class AdminAll(APIView):
	ur = UserRepository()
	ar = AdminRepository()

	@auth_login_required(['admin'])
	def get(self, request):
		status = request.GET['status']
		if status == 'all':
			admin = self.ar.GetAll()
		else:
			admin = self.ar.GetAll(filters=[('admin_status',status)])
		if not admin:
			return Response({"msg":"No admin exists"})
		admin_serialized=AdminSerializer(admin, many=True).data
		return Response(admin_serialized,status=200)


class AdminEdit(APIView):
	ur = UserRepository()
	ar = AdminRepository()

	@auth_login_required(['admin'])
	def get(self, request):
		admin_uuid = request.GET['admin_uuid']
		admin = self.ar.GetFirst(filters=[('uuid',admin_uuid)])
		if not admin:
			return Response({"msg":"No such admin exists"})
		admin_serialized=AdminSerializer(admin).data
		return Response(admin_serialized,status=200)

	@auth_login_required(['admin'])
	def post(self, request):
		admin_uuid = request.data['admin_uuid']
		admin = self.ar.GetFirst(filters=[('uuid',admin_uuid)])
		if not admin:
			return Response({"msg":"No such admin exists"})
		new_role = request.data['new_role']
		admin.admin_type = new_role
		admin.save()
		return Response({"msg":"Admin role changed"},status=200)


class AdminDelete(APIView):
	ur = UserRepository()
	ar = AdminRepository()
	@auth_login_required(['admin'])
	def delete(self, request, admin_uuid):
		admin = self.ar.GetFirst(filters=[('uuid',admin_uuid)])
		if not admin:
			return Response({"msg":"No such admin exists"})
		user = admin.user
		if not user:
			return Response({"msg":"No user exists for this admin account"})
		admin.delete()
		user.delete()
		return Response({"msg":"Admin deleted"},status=200)