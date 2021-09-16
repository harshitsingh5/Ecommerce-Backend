from django.db import models as db
from django.contrib.auth.models import AbstractBaseUser
from django.core import validators
from django.core.validators import RegexValidator
from datetime import datetime
from django.core.exceptions import ValidationError
from tinymce import models as tinymce_models
from polymorphic.models import PolymorphicModel
from .enumerations import *
import jsonfield as j
import re
from shortuuidfield import ShortUUIDField
import os
from uuid import uuid4

def numeric(value):
	reg = re.compile('^[0-9]+$')
	if not reg.match(value) :
		raise ValidationError(
			_('Only Digits Allowed.'),
			params={'value': value},
		)

def alpha(value):
	reg = re.compile('^[a-zA-Z]+$')
	if not reg.match(value) :
		raise ValidationError(
			_('Only Alphabets Allowed.'),
			params={'value': value},
		)

def alphanumeric(value):
	reg = re.compile('^[a-zA-Z0-9]+$')
	if not reg.match(value) :
		raise ValidationError(
			_('Only Alphanumeric Allowed.'),
			params={'value': value},
		)
#numeric = RegexValidator(r'^[0-9]+$', 'Only digits.')
#alpha = RegexValidator(r'^[a-zA-Z]+$', 'Only Alphabets.')
#alphanumeric = RegexValidator(r'^[a-zA-Z0-9]+$', 'Only Alphanumeric')


class User(AbstractBaseUser):
	uuid = ShortUUIDField()
	name = db.CharField(max_length=100, blank=True,null=True)
	email_id = db.CharField(max_length=50, unique=True)
	mobile_number = db.CharField(max_length=13, blank=True,null=True)
	password = db.CharField(max_length=250, blank=True,null=True)
	status = db.CharField(default='email_unverified', max_length=40, blank=True, choices=User_status.choices())
	address = j.JSONField(null=True, blank=True)
	#bookings = OneToMany with bookings table
	#orders = OneToMany with orders table
	#cart = OneToOne with cart table
	#coupons = ManyToMany with Coupons
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	USERNAME_FIELD = 'email_id'
	REQUIRED_FIELDS = []

	def get_role(self):
		if self.admin.first():
			return 'admin'
			# return self.admin.first().admin_type
		return "user"

	def user_id(self):
		return self.uuid


class Admin(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='admin')	#one-to-one with user
	admin_type = db.CharField(max_length=40, blank=True, choices=Admin_type_enum.choices())
	admin_status = db.IntegerField(default=1, blank=True,null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)


class Otp(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='otp')   #one-to-one with user
	otp = db.CharField(max_length=8, blank=True,null=True)
	token = db.CharField(max_length=50, blank=True,null=True)
	valid_till = db.DateTimeField(blank=True,null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='otp_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='otp_updations')


class Service(PolymorphicModel):
	uuid = ShortUUIDField()
	service_name = db.CharField(max_length=100, blank=True,null=True)
	# description = db.TextField(blank=True,null=True)
	# why_use = j.JSONField(null=True, blank=True)
	# video_link = db.CharField(max_length=100,blank=True,null=True)
	#bookings = OneToMany with bookings
	solutions = db.CharField(max_length=40, blank=True,null=True, choices=Solution.choices())
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='service_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='service_updations')


class Coupons(db.Model):
	uuid = ShortUUIDField()
	coupon_code = db.CharField(max_length=100)
	min_amount = db.FloatField()
	max_amount = db.FloatField()
	coupon_type = db.IntegerField(default=2)		# 1-percent-based, 2-amount-based
	discount_percent = db.FloatField(null=True)
	max_discounted_amount = db.FloatField()
	max_users = db.IntegerField()
	per_user_limit = db.IntegerField(default=1)
	description = db.TextField(null=True)
	coupon_status = db.CharField(max_length=40, blank=True,null=True, choices=Coupon_status_enum.choices())
	users = db.ManyToManyField(User, blank=True,  related_name='coupons')
	#orders = OneToMany with orders
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='coupons_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='coupons_updations')



class Orders(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='orders')
	status = db.CharField(max_length=40, blank=True,null=True, choices=Order_status.choices())
	#order_items = OneToMany with bookings
	#payments = OneToMany with Payments
	coupon = db.ForeignKey(Coupons, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='orders')
	address = j.JSONField(null=True, blank=True)
	total_amount = db.FloatField(blank=True,null=True)
	discounted_amount = db.FloatField(blank=True,null=True)
	advance_amount = db.FloatField(blank=True,null=True)
	installment1_amount = db.FloatField(blank=True,null=True)
	installment2_amount = db.FloatField(blank=True,null=True)
	remaining_amount = db.FloatField(blank=True,null=True)       #last 25% of payment
	order_payment_status = db.CharField(max_length=40, blank=True,null=True, choices=Order_payment_status_enum.choices())
	tracking_url = db.CharField(max_length=100)
	tracking_description = db.TextField(null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='order_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='order_updations')


class Cart(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='cart')
	status = db.CharField(max_length=40, blank=True,null=True, choices=Cart_status.choices())
	#cart_items = OneToMany with bookings
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='cart_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='cart_updations')


class Cnc(Service):
	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Cnc_services.choices())
	technology = db.CharField(max_length=40, blank=True,null=True, choices=Cnc_technology.choices())
	material = db.CharField(max_length=40, blank=True,null=True, choices=Cnc_material.choices())
	colour = db.CharField(max_length=40, blank=True,null=True, choices=Cnc_colour.choices())
	bed_size = db.CharField(max_length=40, blank=True,null=True, choices=Cnc_bed_size.choices())
	quantity = db.IntegerField(blank=True, null=True)
	

class Laser_cutting(Service):
	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Laser_cutting_services.choices())
	material = db.CharField(max_length=40, blank=True,null=True, choices=Laser_cutting_material.choices())
	bed_size = db.CharField(max_length=40, blank=True,null=True, choices=Laser_cutting_bed_size.choices())


class Pcb_designing(Service):
	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Pcb_designing_services.choices())


class Three_d_printing(Service):
	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_services.choices())
	technology = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_technology.choices())
	material = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_material.choices())
	colour = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_colour.choices())
	bed_size = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_bed_size.choices())
	layer_height = db.CharField(max_length=40, blank=True,null=True, choices=Three_d_printing_layer_height.choices())
	quantity = db.IntegerField(blank=True, null=True)


# class Rapid_prototyping(Service):
# 	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Rapid_prototyping_services.choices())
# 	details = db.TextField(blank=True,null=True)


class Web_mobile(Service):
	selected_service = db.CharField(max_length=40, blank=True,null=True, choices=Web_mobile_services.choices())


def path_and_rename(path):
	def wrapper(instance, filename):
		ext = filename.split('.')[-1]
		# get filename
		if instance.pk:
			filename = '{}.{}'.format(instance.pk, ext)
		else:
			# set filename as random string
			filename = '{}.{}'.format(uuid4().hex, ext)
		# return the whole path to the file
		return os.path.join(path, filename)
	return wrapper
	# return path+str(uuid4())

class Bookings(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='bookings')
	service = db.ForeignKey(Service, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='bookings')
	# bookingeable_type = db.CharField(max_length=40, blank=True,null=True, choices=Bookingeable_type_enum.choices())
	# bookingeable_id = db.IntegerField(blank=True,null=True)
	uploaded_file = db.FileField(null=True, upload_to=path_and_rename('booking/'))
	order = db.ForeignKey(Orders, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='order_items')
	cart = db.ForeignKey(Cart, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='cart_items')
	status = db.CharField(max_length=40, blank=True,null=True, choices=Booking_status.choices())
	amount = db.FloatField(blank=True,null=True)
	#quote = OneToMany with Quotations
	# ip_address = db.CharField(max_length=20, blank=True,null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='bookings_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='bookings_updations')



class Rapid_proto(db.Model):
	uuid = ShortUUIDField()
	name = db.CharField(max_length=100, blank=True,null=True)
	email_id = db.CharField(max_length=50)
	mobile_number = db.CharField(max_length=13, blank=True,null=True)
	project_type = db.TextField(blank=True,null=True)
	description = db.TextField(blank=True,null=True)
	uploaded_file = db.FileField(null=True, upload_to=path_and_rename('rapidproto/'))
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='bookings_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='bookings_updations')



class Payments(db.Model):
	uuid = ShortUUIDField()
	order = db.ForeignKey(Orders, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='payments')
	mode = db.CharField(max_length=100,null=True)
	amount = db.FloatField(blank=True,null=True)
	order_creation_json = j.JSONField(null=True, blank=True)
	payment_json = j.JSONField(null=True, blank=True)
	razorpay_order_id = db.CharField(max_length=100,null=True, blank=True)
	status = db.CharField(max_length=40, blank=True,null=True, choices=Payment_status_enum.choices())
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='payments_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='payments_updations')


class Quotation(db.Model):
	uuid = ShortUUIDField()
	booking = db.ForeignKey(Bookings, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='quote')
	admin = db.ForeignKey(Admin, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='quotes')
	amount = db.FloatField(blank=True,null=True)
	description = db.TextField()
	status = db.CharField(max_length=40, blank=True,null=True, choices=Quotation_status.choices())
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='quotation_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='quotation_updations')


class Consultation(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='consultations')
	domain = db.CharField(max_length=40, blank=True, choices=Consultation_domain_enum.choices())
	start_time = db.DateTimeField(blank=True,null=True)
	end_time = db.DateTimeField(blank=True,null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='consultation_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='consultation_updations')


class Contact_us(db.Model):
	uuid = ShortUUIDField()
	name = db.CharField(max_length=100)
	email_id = db.CharField(max_length=50, blank=True,null=True)
	mobile_number = db.CharField(max_length=13, unique=True)
	domain = db.CharField(max_length=40, blank=True,null=True, choices=Contact_us_domain_enum.choices())
	description=db.TextField(blank=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='contact_us_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='contact_us_updations')


class Blogs(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='blogs')
	# user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='blogs')
	heading = db.CharField(max_length=100,blank=True, null=True)
	slug = db.TextField(blank=True, null=True)
	thumbnail= db.CharField(max_length=200,blank=True, null=True)
	html_data = tinymce_models.HTMLField(blank=True)
	#comments = OneToMany with Comments
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='blogs_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='blogs_updations')


class Comments(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='comments')
	blog = db.ForeignKey(Blogs, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='comments')
	comment_data = db.TextField(blank=True,null=True)
	#replies = OneToMany with Replies
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='comments_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='comments_updations')


class Replies(db.Model):
	uuid = ShortUUIDField()
	user = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='replies')
	comment = db.ForeignKey(Comments, on_delete=db.DO_NOTHING, blank=True, null=True, related_name='replies')
	reply_data = db.TextField(blank=True,null=True)
	created_at = db.DateTimeField(auto_now_add=True)
	updated_at = db.DateTimeField(auto_now=True)
	# created_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='replies_creations')
	# updated_by = db.ForeignKey(User, on_delete=db.DO_NOTHING, blank=True, related_name='replies_updations')











#
