from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
# from django.contrib.gis.utils import GeoIP
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.fields import CurrentUserDefault
from django.db import transaction
from ieomanager.Serializers import *
from ieomanager.models import *
from ieomanager.repository import *
# from datetime import datetime,timedelta
from django.utils import timezone
from ieomanager.permisions import IsAdminOrOwner
from functools import partial
from ieomanager.utilities import auth_login_required
import json
from rest_framework import parsers
from django.views.decorators.csrf import csrf_exempt
import razorpay

live_key_id="rzp_live_dummy"
live_key_secret="dummy"

test_key_id="rzp_test_dummy"
test_key_secret="dummy"

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def get_eable_object(eable_type):
	x = None
	if eable_type=='Bookingeable_type_enum.Cnc':
		x = CncRepository()
	if eable_type=='Bookingeable_type_enum.Laser_cutting':
		x = Laser_cuttingRepository()
	if eable_type=='Bookingeable_type_enum.Pcb_designing':
		x = Pcb_designingRepository()
	if eable_type=='Bookingeable_type_enum.Three_d_printing':
		x = Three_d_printingRepository()
	if eable_type=='Bookingeable_type_enum.Web_mobile':
		x = Web_mobileRepository()
	if eable_type=='Bookingeable_type_enum.Rapid_prototyping':
		x = Rapid_prototypingRepository()
	return x

# to create serialized data
def get_eable_serializer1(eable_type,data):
	x=None
	if eable_type=='Bookingeable_type_enum.Cnc':
		x = CncSerializer(data=data)
	if eable_type=='Bookingeable_type_enum.Laser_cutting':
		x = Laser_cuttingSerializer(data=data)
	if eable_type=='Bookingeable_type_enum.Pcb_designing':
		x = Pcb_designingSerializer(data=data)
	if eable_type=='Bookingeable_type_enum.Three_d_printing':
		x = Three_d_printingSerializer(data=data)
	if eable_type=='Bookingeable_type_enum.Web_mobile':
		x = Web_mobileSerializer(data=data)
	# if eable_type=='Bookingeable_type_enum.Rapid_prototyping':
	# 	x = Rapid_prototypingSerializer(data=data)
	return x


# to get serialized data
def get_eable_serializer2(eable_type, database_object):
	x=None
	if eable_type=='Bookingeable_type_enum.Cnc':
		x = CncSerializer(database_object)
	if eable_type=='Bookingeable_type_enum.Laser_cutting':
		x = Laser_cuttingSerializer(database_object)
	if eable_type=='Bookingeable_type_enum.Pcb_designing':
		x = Pcb_designingSerializer(database_object)
	if eable_type=='Bookingeable_type_enum.Three_d_printing':
		x = Three_d_printingSerializer(database_object)
	if eable_type=='Bookingeable_type_enum.Web_mobile':
		x = Web_mobileSerializer(database_object)
	# if eable_type=='Bookingeable_type_enum.Rapid_prototyping':
	# 	x = Rapid_prototypingSerializer(database_object)
	return x


class EditProfile(APIView):
	@auth_login_required(['user','admin'])
	def put(self, request):
		user=request.user
		serializer = UserEditSerializer(user,data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['email_id']:
			user = serializer.save()
			serializer = UserEditSerializer(user)
			return Response({"msg":"Profile Updated","user":serializer.data}, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

#view all services
class Services_view_all(APIView):
	sr=ServiceRepository()
	def get(self,request):
		services = self.sr.GetAll()
		serializer = ServicePolymorphicSerializer(services, many=True)
		return Response(serializer.data)
		# return Response(UserSerializer(request.user).data)

#view all Bookings
class Bookings_view_all(APIView):
	br=BookingsRepository()
	def get(self,request):
		bookings = self.br.GetAll()
		serializer = BookingsSerializer(bookings, many=True)
		return Response(serializer.data)


class User_bookings(APIView):
	br=BookingsRepository()
	qr=QuotationRepository()
	# ur = UserRepository()
	parser_classes = (parsers.MultiPartParser,)
	#view Bookings of particular User
	@auth_login_required(['user','admin'])
	def get(self,request):
		user=request.user
		bookings = user.bookings.all()
		# if request.GET.get('include'):
		# 	bookings = BookingsSerializer.setup_eager_loading(bookings)
		data = BookingsSerializer(bookings, many=True).data
		return Response({"data":data})

		# d=[]
		# x=None
		# for b in bookings:
		#     serializer = BookingsSerializer(b)
		#     x=b.bookingeable_type
		#     self.obj = get_eable_object(eable_type=x)
		#     detail_obj = self.obj.GetFirst(filters=[('id',b.bookingeable_id)])
		#     s = get_eable_serializer2(b.bookingeable_type,detail_obj)
		#     d.append({"booking":serializer.data, "booking_detail":s.data})
		# return Response({"Booking List":d})

	#add a booking
	@auth_login_required(['user','admin'])
	def post(self, request):
		# obj = get_eable_object(request.data['eable_type'])
		user=request.user
		# user = self.ur.GetFirst(filters=[('uuid',user_uuid)])
		# return Response({"msg":json.loads(request.data["data"])})
		serializer = get_eable_serializer1(request.data['eable_type'],json.loads(request.data['data']))
		serializer.is_valid(raise_exception=True)
		# return Response({"msg":"hello"})
		# if serializer.validated_data:
		with transaction.atomic():
			service_object = serializer.save()
			booking_object = self.br.Create(values={
													"user":user,
													# "bookingeable_type":request.data['eable_type'],
													# "bookingeable_id":service_object.id,
													"service":service_object,
													"uploaded_file": request.data["file"],
													"status":request.data['status']
													})
			bs = BookingsSerializer(booking_object)
			# ss = get_eable_serializer2(request.data['eable_type'],service_object)
			if request.data['status']=='Booking_status.in_booking':
				quotation_object = self.qr.Create(values={
													"booking":booking_object,
													"status":Quotation_status.not_started,
													"amount":0.0
													})
			return Response(bs.data, status=201)
		return Response({"msg":"Invalid Data"}, status=400)


class User_filtered_bookings(APIView):
	br=BookingsRepository()

	#view filtered Bookings of particular User
	@auth_login_required(['user','admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			bookings=self.br.GetAll(filters=[('user',user)])
		else:
			bookings = self.br.GetAll(filters=[('user',user),('status',status)])
		data = BookingsSerializer(bookings, many=True).data
		return Response(data)


class Admin_bookings(APIView):
	br=BookingsRepository()

	#view filtered Bookings for Admin
	@auth_login_required(['admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			bookings=self.br.GetAll()
		else:
			bookings = self.br.GetAll(filters=[('status',status)])
		data = BookingsSerializer(bookings, many=True).data
		return Response(data)


class Admin_orders(APIView):
	orr=OrdersRepository()

	#view all orders
	@auth_login_required(['admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			orders=self.orr.GetAll(filters=[])
		else:
			orders=self.orr.GetAll(filters=[('status',status)])
		orders_serialized = OrdersSerializer(orders, many=True)
		return Response(orders_serialized.data)


class User_bookings_details(APIView):
	br=BookingsRepository()
	# ur = UserRepository()

	#view a particular booking
	@auth_login_required(['user','admin'])
	def get(self,request, booking_uuid):
		user=request.user
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		data = BookingsSerializer(booking).data
		return Response(data)

	#edit a particular booking
	@auth_login_required(['user','admin'])
	def put(self, request, booking_uuid):
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		serializer = BookingsSerializer(booking,data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data:
			booking = serializer.save()
			serializer = BookingsSerializer(booking)
			return Response({"msg":"booking Updated","booking_details":serializer.data}, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

	#delete a booking
	@auth_login_required(['user','admin'])
	def delete(self, request, booking_uuid):
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		if not booking:
			return Response({"msg":"Booking not found"}, status=400)
		service=booking.service
		booking.delete()
		service.delete()
		return Response({"msg":"Booking deleted"}, status=201)





#CART IMPLEMENTATION
class User_Cart(APIView):
	cr=CartRepository()
	# ur = UserRepository()

	#view items in cart
	@auth_login_required(['user','admin'])
	def get(self,request):
		user=request.user
		cart = self.cr.GetFirst(filters=[('user',user)])
		bookings_in_cart = cart.cart_items.all()
		bookings_serialized = BookingsSerializer(bookings_in_cart, many=True)
		return Response(bookings_serialized.data)


class CartFunc(APIView):
	cr = CartRepository()
	br = BookingsRepository()

	#add a booking to cart
	@auth_login_required(['user','admin'])
	def post(self, request, booking_uuid):
		user = request.user
		cart = self.cr.GetFirst(filters=[('user',user)])
		if not cart:
			return Response({"msg":"Cart of user does not exist"})
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		if not booking:
			return Response({"msg":"No such booking exists"})
		booking.status=Booking_status.in_cart
		booking.save()
		cart.cart_items.add(booking)
		return Response({"msg":"booking added to cart"})


	#remove a booking from cart
	@auth_login_required(['user','admin'])
	def delete(self, request, booking_uuid):
		user = request.user
		cart = self.cr.GetFirst(filters=[('user',user)])
		if not cart:
			return Response({"msg":"Cart of user does not exist"})
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		if not booking:
			return Response({"msg":"No such booking exists"})
		booking.status='Booking_status.in_booking'
		booking.save()
		cart.cart_items.remove(booking)
		return Response({"msg":"booking removed from cart"})


class Change_booking_status(APIView):
	br = BookingsRepository()
	cr = CartRepository()
	qr = QuotationRepository()

	@auth_login_required(['user','admin'])
	def post(self, request, booking_uuid):
		user = request.user
		booking = self.br.GetFirst(filters=[('uuid',booking_uuid)])
		if not booking:
			return Response({"msg":"No such booking exists"})
		data= json.loads(request.body)
		old_status = data['old_status']
		new_status = data['new_status']

		#LIST TO BOOKING
		if old_status=="Booking_status.in_list" and new_status=="Booking_status.in_booking":
			with transaction.atomic():
				booking.status=new_status
				booking.save()
				quotation_object = self.qr.Create(values={
														"booking":booking,
														"status":Quotation_status.not_started,
														"amount":0.0
														})
				return Response({"msg":"quotation sent, booking status updated"})

		if old_status=="Booking_status.in_booking" and new_status=="Booking_status.quote_obtained":
			with transaction.atomic():
				booking.status=new_status
				booking.save()
				return Response({"msg":"quotation obtained, booking status updated"})

		#BOOKING(QUOTE_OBTAINED) TO CART       i.e. ADD_TO_CART implementation
		if old_status=="Booking_status.quote_obtained" and new_status=="Booking_status.in_cart":
			with transaction.atomic():
				booking.status=new_status
				booking.save()
				cart = self.cr.GetFirst(filters=[('user',user)])
				if not cart:
					return Response({"msg":"Cart of user does not exist"})
				cart.cart_items.add(booking)
				return Response({"msg":"added to cart, booking status updated"})

		#CART TO BOOKING(QUOTE_OBTAINED)       i.e. REMOVE_FROM_CART implementation
		if old_status=="Booking_status.in_cart" and new_status=="Booking_status.quote_obtained":
			with transaction.atomic():
				booking.status=new_status
				booking.save()
				cart = self.cr.GetFirst(filters=[('user',user)])
				if not cart:
					return Response({"msg":"Cart of user does not exist"})
				cart.cart_items.remove(booking)
				return Response({"msg":"added to cart, booking status updated"})

		return Response({"msg":"Sorry Status Change not possible"})

class Admin_quotes(APIView):
	qr=QuotationRepository()

	#view all quotations
	@auth_login_required(['admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			quotations = self.qr.GetAll()
		else:
			quotations = self.qr.GetAll(filters=[('status',status)])
		quotations_serialized = QuotationSerializer(quotations, many=True)
		return Response(quotations_serialized.data)


class Admin_quote_details(APIView):
	qr=QuotationRepository()

	#add a quote
	@auth_login_required(['admin'])
	def put(self, request, quotation_uuid):
		quotation = self.qr.GetFirst(filters=[('uuid',quotation_uuid)])
		serializer = QuotationSerializer(quotation,data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data:
			with transaction.atomic():
				booking=quotation.booking
				booking.status=Booking_status.quote_obtained
				booking.save()
				quotation = serializer.save()
				serializer = QuotationSerializer(quotation)
				return Response({"msg":"Quotation Given","quotation":serializer.data}, status=201)
		return Response({"msg":"Invalid Data"}, status=400)




class Orderss(APIView):
	orr=OrdersRepository()

	#view all orders
	@auth_login_required(['user','admin'])
	def get(self,request,status):
		user=request.user
		if status == 'all':
			orders=self.orr.GetAll(filters=[('user',user)])
		else:
			orders=self.orr.GetAll(filters=[('user',user),('status',status)])
		orders_serialized = OrdersSerializer(orders, many=True)
		return Response(orders_serialized.data)

	@auth_login_required(['user','admin'])
	def post(self,request,status):
		user=request.user
		order_serialized=None
		with transaction.atomic():
			amount = 0.0
			for b in user.cart.first().cart_items.all():
				b.status=Booking_status.in_order
				b.save()
				amount = amount + b.quote.first().amount
			new_order = self.orr.Create(values={
												"user":user,
												"status":'unpaid',
												"total_amount":amount,
												"discounted_amount":amount
												})
			for b in user.cart.first().cart_items.all():
				new_order.order_items.add(b)
				new_order.save()
				# user.cart.first().cart_items.remove(b)
			order_serialized = OrdersSerializer(new_order)
		return Response({
			"data":order_serialized.data
		})
			
			
class Order_details(APIView):
	orr=OrdersRepository()

	#view all orders
	@auth_login_required(['user','admin'])
	def get(self,request,order_uuid):
		user=request.user
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		order_serialized = OrdersSerializer(order)
		bookings_in_order = order.order_items.all()
		bookings_serialized = BookingsSerializer(bookings_in_order, many=True)
		return Response({"order":order_serialized.data,"bookings":bookings_serialized.data})


class Order_add_address(APIView):
	orr=OrdersRepository()
	pr=PaymentsRepository()

	@auth_login_required(['user','admin'])
	def post(self,request,order_uuid):
		user=request.user
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not order:
			return Response({"msg":"No such order found"})
		with transaction.atomic():
			new_payment = self.pr.Create(values={
												"order":order,
												"status":'awaited'
												})
			order.address=request.data['order_address']
			order.save()
			for b in user.cart.first().cart_items.all():
				user.cart.first().cart_items.remove(b)
		return Response({
			"msg":"Order Address added, payment awaited"
		})


class Order_payment(APIView):
	orr=OrdersRepository()
	pr=PaymentsRepository()
	@auth_login_required(['user','admin'])
	def post(self, request, order_uuid):
		user=request.user
		orderr=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not orderr:
			return Response({"msg":"No such order found"})
		amount = int(orderr.discounted_amount) * 100
		client = razorpay.Client(auth=(test_key_id,test_key_secret))
		payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
		payment_obj = self.pr.GetFirst(filters=[('order',orderr)])
		payment_obj.mode = 'razorpay'
		payment_obj.amount = amount
		payment_obj.order_creation_json = payment
		payment_obj.razorpay_order_id = payment['id']
		payment_obj.save()
		user_serialized=UserSerializer(user).data
		cu='http://xyz.in:5000/api/v1/users/order-callback'
		return Response({"payment":payment,"user":user_serialized,"callback_url":cu})


class Order_callback(APIView):
	orr=OrdersRepository()
	pr=PaymentsRepository()
	@auth_login_required(['user','admin'])
	def post(self, request):
		data=json.loads(request.body)
		# data = request.data
		if data:
			razorpay_payment_id=data['razorpay_payment_id']
			razorpay_order_id=data['razorpay_order_id']
			razorpay_signature=data['razorpay_signature']
			# payment_obj = Payments.objects.first()
			payment_obj = self.pr.GetFirst(filters=[('razorpay_order_id',razorpay_order_id)])
			payment_obj.payment_json=data
			payment_obj.save()
			order=payment_obj.order
			client = razorpay.Client(auth=(test_key_id,test_key_secret))
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': razorpay_payment_id,
				'razorpay_signature': razorpay_signature
			}
			try:
				client.utility.verify_payment_signature(params_dict)
				with transaction.atomic():
					payment_obj.status='successful'
					order.order_payment_status='full_payment_received'
					order.status='placed'
					payment_obj.save()
					order.save()
					return Response({"msg":"payment received successfully"})
				return Response({"msg":"payment received but backend server error"})
			except:
				payment_obj.status='failed'
				payment_obj.save()
				return Response({"msg":"payment unsuccessful"})
		else:
			return Response({"msg":"payment unsuccessful"})





class Change_order_status(APIView):
	orr=OrdersRepository()

	@auth_login_required(['admin'])
	def post(self, request, order_uuid):
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not order:
			return Response({"msg":"No such order found"})
		data= json.loads(request.body)
		order.status= data['new_status']
		order.save()
		return Response({"msg":"order status updated"})



class Cancel_order(APIView):
	orr=OrdersRepository()

	@auth_login_required(['user','admin'])
	def post(self, request, order_uuid):
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not order:
			return Response({"msg":"No such order found"})
		order.status= 'cancelled'
		order.save()
		return Response({"msg":"order status updated"})





# COUPONS IMPLEMENTATION
class Coupon_admin(APIView):
	cr=CouponsRepository()

	#view all coupon
	@auth_login_required(['admin'])
	def get(self,request,status):
		# user=request.user
		if status == 'all':
			coupons = self.cr.GetAll()
		else:
			coupons = self.cr.GetAll(filters=[('coupon_status',status)])
		coupons_serialized = CouponsSerializer(coupons, many=True)
		return Response(coupons_serialized.data)

	#add a coupon
	@auth_login_required(['admin'])
	def post(self,request,status):
		# user=request.user
		serializer = CouponsSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data:
			coupon = serializer.save()
			serializer = CouponsSerializer(coupon)
			return Response(serializer.data, status=201)
		return Response({"msg":"Invalid Data"}, status=400)


class Coupon_admin_details(APIView):
	cr=CouponsRepository()

	# view coupon
	@auth_login_required(['admin'])
	def get(self, request, coupon_uuid):
		coupon = self.cr.GetFirst(filters=[('uuid',coupon_uuid)])
		if not coupon:
			return Response({"msg":"No such coupon exists"})
		coupon_serialized=CouponsSerializer(coupon)
		return Response(coupon_serialized.data)

	# change coupon status
	@auth_login_required(['admin'])
	def post(self, request, coupon_uuid):
		coupon = self.cr.GetFirst(filters=[('uuid',coupon_uuid)])
		if not coupon:
			return Response({"msg":"No such coupon exists"})
		coupon.coupon_status=request.data['new_status']
		coupon.save()
		return Response({"msg":"coupon status updated"})


	#delete a coupon
	@auth_login_required(['admin'])
	def delete(self, request, coupon_uuid):
		coupon = self.cr.GetFirst(filters=[('uuid',coupon_uuid)])
		if not coupon:
			return Response({"msg":"No such coupon exists"})
		coupon.delete()
		return Response({"msg":"coupon deleted"})


class Coupon_user(APIView):
	cr=CouponsRepository()
	orr=OrdersRepository()

	#apply coupon
	@auth_login_required(['admin','user'])
	def post(self,request,order_uuid):
		user=request.user
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not order:
			return Response({"msg":"No such order found"})
		amount=order.total_amount
		discount=0.0
		coupon_code=request.data['coupon_code']
		coupon = self.cr.GetFirst(filters=[('coupon_code',coupon_code)])
		if not coupon:
			return Response({"msg":"No such coupon found"})
		if coupon.coupon_status=='inactive':
			return Response({"msg":"Coupon is inactive"})
		if coupon.coupon_status=='expired':
			return Response({"msg":"Coupon has expired"})
		if user in coupon.users.all():
			return Response({"msg":"User has already used the coupon"})
		if coupon.users.count() >= coupon.max_users:
			return Response({"msg":"Coupon has been used maximum number of times"})
		if order.total_amount < coupon.min_amount or order.total_amount > coupon.max_amount:
			return Response({"msg":"Order amount not valid"})
		if coupon.coupon_type==1:
			discount = amount*coupon.discount_percent/100
			if discount > coupon.max_discounted_amount:
				discount = coupon.max_discounted_amount
		elif coupon.coupon_type==2:
			discount = coupon.max_discounted_amount
		discount = round(discount,2)
		with transaction.atomic():
			coupon.orders.add(order)
			coupon.users.add(user)
			order.discounted_amount = order.total_amount-discount
			order.save()
			return Response({"msg":"Coupon applied successfully","discount":discount,"old_amount":amount,"new_amount":order.discounted_amount})


	# remove an applied coupon
	@auth_login_required(['admin','user'])
	def delete(self,request,order_uuid,coupon_code):
		user=request.user
		order=self.orr.GetFirst(filters=[('uuid',order_uuid)])
		if not order:
			return Response({"msg":"No such order found"})
		coupon = self.cr.GetFirst(filters=[('coupon_code',coupon_code)])
		if not coupon:
			return Response({"msg":"No such coupon found"})
		if not order.coupon == coupon:
			return Response({"msg":"This coupon is not aoplied to your order"})
		with transaction.atomic():
			coupon.orders.remove(order)
			coupon.users.remove(user)
			order.discounted_amount = order.total_amount
			order.coupon=None
			order.save()
			return Response({"msg":"Coupon removed","old_amount":order.total_amount,"new_amount":order.discounted_amount})



# Rapid prototyping IMPLEMENTATION---------------------------------------------------------
class Rapid_prototyping(APIView):
	cr=Rapid_prototypingRepository()
	parser_classes = (parsers.MultiPartParser,)

	#view all rapid protos
	@auth_login_required(['admin'])
	def get(self,request):
		# user=request.user
		rapid_protos = self.cr.GetAll()
		rapid_protos_serialized = Rapid_prototypingSerializer(rapid_protos, many=True)
		return Response(rapid_protos_serialized.data)

	#add a rapid proto
	# @auth_login_required(['user','admin'])
	def post(self,request):
		# user=request.user
		serializer = Rapid_prototypingSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data:
			rapid_protos = self.cr.Create(values={
												"name":request.data['name'],
												"email_id":request.data['email_id'],
												"mobile_number":request.data['mobile_number'],
												"project_type":request.data['project_type'],
												"description":request.data['description'],
												"uploaded_file": request.data["file"]
												 })
			serializer = Rapid_prototypingSerializer(rapid_protos)
			return Response(serializer.data, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

class Rapid_prototyping_details(APIView):
	cr=Rapid_prototypingRepository()

	#view particular 
	@auth_login_required(['admin','user'])
	def get(self,request,rapidproto_uuid):
		# user=request.user
		rapid_protos = self.cr.GetFirst(filters=[('uuid',rapidproto_uuid)])
		rapid_protos_serialized = Rapid_prototypingSerializer(rapid_protos)
		return Response(rapid_protos_serialized.data)







#Consultation IMPLEMENTATION---------------------------------------------------------------
class Consultations(APIView):
	cr=ConsultationRepository()

	#view all consultations
	@auth_login_required(['admin','user'])
	def get(self,request):
		user=request.user
		consultations = self.cr.GetAll()
		consultations_serialized = ConsultationSerializer(consultations, many=True)
		return Response(consultations_serialized.data)

	#add a consultation
	@auth_login_required(['user','admin'])
	def post(self,request):
		user=request.user
		serializer = ConsultationSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['start_time'] and serializer.validated_data['end_time']:
			consultation = serializer.save()
			serializer = ConsultationSerializer(consultation)
			return Response(serializer.data, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

class Consultation_details(APIView):
	cr=ConsultationRepository()

	#view particular consultation
	@auth_login_required(['admin','user'])
	def get(self,request,consultation_uuid):
		user=request.user
		consultation = self.cr.GetFirst(filters=[('uuid',consultation_uuid)])
		consultation_serialized = ConsultationSerializer(consultation)
		return Response(consultation_serialized.data)



#Contact_us IMPLEMENTATION
class Contact_uss(APIView):
	cr=Contact_usRepository()

	#view all contact_us
	@auth_login_required(['admin'])
	def get(self,request):
		# user=request.user
		contactus_all = self.cr.GetAll()
		contactus_serialized = Contact_usSerializer(contactus_all, many=True)
		return Response(contactus_serialized.data)

	#add a contact_us
	@auth_login_required(['user','admin'])
	def post(self,request):
		# user=request.user
		serializer = Contact_usSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['email_id'] and serializer.validated_data['description']:
			contact_us = serializer.save()
			serializer = Contact_usSerializer(contact_us)
			return Response(serializer.data, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

class Contact_us_details(APIView):
	cr=Contact_usRepository()

	#view particular contact_us
	@auth_login_required(['admin'])
	def get(self,request,contact_us_uuid):
		# user=request.user
		contactus = self.cr.GetFirst(filters=[('uuid',contact_us_uuid)])
		contactus_serialized = Contact_usSerializer(contactus)
		return Response(contactus_serialized.data)


#
