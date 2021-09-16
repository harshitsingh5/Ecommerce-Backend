from .baseRepository import BaseRepository
from ieomanager.models import Otp

class OtpRepository(BaseRepository):
    def __init__(self):
        self.model = Otp