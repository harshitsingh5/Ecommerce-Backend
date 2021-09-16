
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions
from ieomanager.models import User_status
from rest_framework.response import Response
from ieomanager.repository import UserRepository,OtpRepository,AdminRepository
import bcrypt


class AdminLoginSerializer(serializers.Serializer):
    repository=UserRepository()
    adminrepo=AdminRepository()
    #validation of data from front end
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        email = data.get("email","")    #for handling key error of email field
        password = data.get("password","")
        if email and password:
            user = self.authenticate(email,password)
            data['user']=None
            if user:
                if user.status == "User_status.email_verified":
                    data['user'] = user
                    return data
                else:
                    msg = "Account Not Verified"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Invalid Credentials"
                raise exceptions.ValidationError(msg)
            pass
        else:
            msg="Email and Password is required"
            raise exceptions.ValidationError(msg)
        return data

    def authenticate(self,email,password):
        user = self.repository.Query(filters=[('email_id',email)]).first()
        if not user:
            return False
        admin = self.adminrepo.Query(filters=[('user',user)]).first()
        if not admin:
            return False
        password=password
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return False


class LoginSerializer(serializers.Serializer):
    repository=UserRepository()
    #validation of data from front end
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        email = data.get("email","")    #for handling key error of email field
        password = data.get("password","")
        if email and password:
            user = self.authenticate(email,password)
            data['user']=None
            if user:
                if user.status == "User_status.email_verified":
                    data['user'] = user
                    return data
                else:
                    msg = "Account Not Verified"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Invalid Credentials"
                raise exceptions.ValidationError(msg)
            pass
        else:
            msg="Email and Password is required"
            raise exceptions.ValidationError(msg)
        return data

    def authenticate(self,email,password):
        user = self.repository.Query(filters=[('email_id',email)]).first()
        if not user:
            return False
        password=password
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return False


class SignUpSerializer(serializers.Serializer):
    repository=UserRepository()
    name=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    mobile_number = serializers.CharField()

    def validate(self,data):
        email = data.get('email','')
        password = data.get('password','')
        mobile_number = data.get('mobile_number','')

        if not email:
            raise exceptions.ValidationError("Email is required")
        elif not password:
            raise exceptions.ValidationError("Password is required")
        elif not mobile_number:
            raise exceptions.ValidationError("Mobile Number is required")
        if self.repository.GetFirst(filters=[('email_id',email)]):
            user = self.repository.GetFirst(filters=[('email_id',email)])
            if user.status == "User_status.email_verified":
                raise exceptions.ValidationError("Email id Already Verified, Please Login")
        return data


class OtpVerifySerializer(serializers.Serializer):
    repository=OtpRepository()
    email=serializers.EmailField()
    otp=serializers.CharField()

    def validate(self,data):
        email = data.get('email','')
        otp = data.get('otp','')
        if not otp:
            raise exceptions.ValidationError("Otp is required")
        elif not email:
            raise exceptions.ValidationError("Email is required")
        return data










#
