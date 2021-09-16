from ieomanager.models import User,Orders,Cart,Bookings,Payments,Coupons,Quotation,Consultation,Contact_us,Rapid_proto
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .ServiceSerializer import *
from .UserSerializer import *

class QuotationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Quotation
		fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payments
		fields = '__all__'

class BookingsSerializer(serializers.ModelSerializer):
	service = ServicePolymorphicSerializer(read_only=True)
	quote = QuotationSerializer(read_only=True,many=True)
	class Meta:
		model = Bookings
		# fields = '__all__'
		fields = ['id','uuid','service','quote','uploaded_file', 'status','created_at','updated_at','user','order','cart']

	@staticmethod
	def setup_eager_loading(queryset):
		queryset = queryset.select_related('service')
		return queryset


class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = '__all__'

class CouponsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupons
		fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
	coupon=CouponsSerializer(read_only=True)
	user=UserSerializer(read_only=True)
	payments=PaymentsSerializer(read_only=True,many=True)
	class Meta:
		model = Orders
		fields = '__all__'


class Rapid_prototypingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rapid_proto
		fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Consultation
		fields = '__all__'

class Contact_usSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact_us
		fields = '__all__'


# class OtpVerifySerializer(serializers.Serializer):
#     repository=OtpRepository()
#     email=serializers.EmailField()
#     otp=serializers.CharField()
#
#     def validate(self,data):
#         email = data.get('email','')
#         otp = data.get('otp','')
#         if not otp:
#             raise exceptions.ValidationError("Otp is required")
#         elif not email:
#             raise exceptions.ValidationError("Email is required")
#         return data
