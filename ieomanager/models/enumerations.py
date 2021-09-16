from enum import Enum

class User_status(Enum):
	email_unverified="email_unverified"          	#only email submitted
	email_verified="email_verified"           		#email verified and mobile unverified
	email_mobile_verified="email_mobile_verified"   #email and mobile both verified
	account_complete="account_complete"          	#address also submitted
	deleted="deleted"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Admin_type_enum(Enum):
	super_admin="super_admin"
	center_admin="center_admin"  #blank now
	service_admin="service_admin" #every service has its own service-admin
	manager="manager"		       #blank now
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Solution(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Bookingeable_type_enum(Enum):
	Cnc="Cnc"
	Laser_cutting="Laser_cutting"
	Pcb_designing="Pcb_designing"
	Three_d_printing="Three_d_printing"
	Web_mobile="Web_mobile"
	Rapid_prototyping="Rapid_prototyping"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Booking_status(Enum):
	unverified='unverified'
	in_list='in_list'
	in_bookings='in_bookings'
	quote_obtained='quote_obtained'
	in_cart='in_cart'
	in_order='in_order'
	verified='verified'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Quotation_status(Enum):
	not_started='not_started'
	in_progress='in_progress'
	accepted='accepted'
	rejected='rejected'
	prepared='prepared'
	submitted='submitted'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Cart_status(Enum):
	pending='pending'
	active='active'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Order_status(Enum):
	unpaid='unpaid'
	placed='placed'
	in_progress='in_progress'
	complete='complete'
	#For cnc, 3d, laser, rapid_prototyping:
	packed='packed'
	shipped='shipped'
	dispatched='dispatched'
	#For pcb and web/app
	under_development='under_development'
	developed='developed'
	testing='testing'
	deployed='deployed'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Order_payment_status_enum(Enum):
	no_payment_received='no_payment_received'
	#each is 25%
	advance_received='advance_received'
	installment1_received='installment1_received'
	installment2_received='installment2_received'
	full_payment_received='full_payment_received'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Payment_status_enum(Enum):
	awaited='awaited'
	successful='successful'
	failed='failed'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Coupon_status_enum(Enum):
	inactive='inactive'
	active='active'
	expired='expired'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Consultation_domain_enum(Enum):
	Cnc='Cnc'
	Laser_cutting='Laser_cutting'
	Pcb_designing='Pcb_designing'
	Three_d_printing='Three_d_printing'
	Web_mobile='Web_mobile'
	# Rapid_prototyping='Rapid_prototyping'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

class Contact_us_domain_enum(Enum):
	Cnc='Cnc'
	Laser_cutting='Laser_cutting'
	Pcb_designing='Pcb_designing'
	Three_d_printing='Three_d_printing'
	Web_mobile='Web_mobile'
	Rapid_prototyping='Rapid_prototyping'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)


#CNC
class Cnc_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Cnc_technology(Enum):
	noDataHere="noDataHere"
	milling='milling'
	turning='turning'
	post_processing='post_processing'
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Cnc_material(Enum):
	noDataHere="noDataHere"
	aluminium="aluminium"
	copper="copper"
	nylon="nylon"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Cnc_colour(Enum):
	noDataHere="noDataHere"
	red="red"
	yellow="yellow"
	green="green"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Cnc_bed_size(Enum):
	noDataHere="noDataHere"
	a30mmx30mmx30mm="a30mmx30mmx30mm"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

#Laser_cutting
class Laser_cutting_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Laser_cutting_material(Enum):
	noDataHere="noDataHere"
	aluminium="aluminium"
	copper="copper"
	nylon="nylon"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Laser_cutting_bed_size(Enum):
	noDataHere="noDataHere"
	a30mmx30mmx30mm="a30mmx30mmx30mm"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

#Pcb_designing
class Pcb_designing_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

#Three_d_printing
class Three_d_printing_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Three_d_printing_technology(Enum):
	noDataHere="noDataHere"
	sls="sls"
	sla="sla"
	fdm="fdm"
	mjf="mjf"
	polyjet="polyjet"
	dmls="dmls"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Three_d_printing_material(Enum):
	noDataHere="noDataHere"
	aluminium="aluminium"
	copper="copper"
	nylon="nylon"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Three_d_printing_colour(Enum):
	noDataHere="noDataHere"
	red="red"
	yellow="yellow"
	green="green"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Three_d_printing_bed_size(Enum):
	noDataHere="noDataHere"
	a30mmx30mmx30mm="a30mmx30mmx30mm"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
class Three_d_printing_layer_height(Enum):
	noDataHere="noDataHere"
	a01mm="a01mm"
	a02mm="a02mm"
	a03mm="a03mm"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

#Rapid_prototyping
class Rapid_prototyping_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)

#Web_mobile
class Web_mobile_services(Enum):
	noDataHere="noDataHere"
	@classmethod
	def choices(cls):
		print(tuple((i.name, i.value) for i in cls))
		return tuple((i.name, i.value) for i in cls)
