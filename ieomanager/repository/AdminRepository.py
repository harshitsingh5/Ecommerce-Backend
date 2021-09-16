from .baseRepository import BaseRepository

from ieomanager.models import Admin

class AdminRepository(BaseRepository):
    def __init__(self):
        self.model= Admin