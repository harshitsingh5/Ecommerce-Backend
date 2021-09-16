from .baseRepository import BaseRepository
from ieomanager.models import User,Orders,Cart,Bookings,Payments,Coupons,Quotation,Consultation,Contact_us

class UserRepository(BaseRepository):
    def __init__(self):
        self.model = User

class OrdersRepository(BaseRepository):
    def __init__(self):
        self.model = Orders

class CartRepository(BaseRepository):
    def __init__(self):
        self.model = Cart

class BookingsRepository(BaseRepository):
    def __init__(self):
        self.model = Bookings

class PaymentsRepository(BaseRepository):
    def __init__(self):
        self.model = Payments

class CouponsRepository(BaseRepository):
    def __init__(self):
        self.model = Coupons

class QuotationRepository(BaseRepository):
    def __init__(self):
        self.model = Quotation

class ConsultationRepository(BaseRepository):
    def __init__(self):
        self.model = Consultation

class Contact_usRepository(BaseRepository):
    def __init__(self):
        self.model = Contact_us
