# from django.contrib.auth.models import User
from ieomanager.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email_id=serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    mobile_number=serializers.IntegerField(validators=[UniqueValidator(queryset=User.objects.all())])
    name = serializers.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['uuid','name', 'email_id','mobile_number','status','address']
        read_only_fields = ['uuid','status']


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid','name', 'email_id','mobile_number','status','address']
        read_only_fields = ['uuid','status']