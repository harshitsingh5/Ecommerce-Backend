from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions
from rest_framework.response import Response
from ieomanager.repository import UserRepository
from ieomanager.models import Admin
from .UserSerializer import UserSerializer


class CreateAdminSerializer(serializers.Serializer):
    repository=UserRepository()
    email=serializers.EmailField()
    password=serializers.CharField()
    mobile_number = serializers.CharField()
    role = serializers.CharField()

    def validate(self,data):
        email = data.get('email','')
        password = data.get('password','')
        mobile_number = data.get('mobile_number','')
        role = data.get('role','')

        if not email:
            raise exceptions.ValidationError("Email is required")
        elif not password:
            raise exceptions.ValidationError("Password is required")
        elif not mobile_number:
            raise exceptions.ValidationError("Mobile Number is required")
        elif not role:
            raise exceptions.ValidationError("Role is required")
        
        user=self.repository.GetFirst(filters=[('email_id',email)])
        if user:
            raise exceptions.ValidationError("Email id Already Added, Please Login")
        return data


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Admin
        fields = '__all__'