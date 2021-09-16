from .baseRepository import BaseRepository
from ieomanager.models import Service,Cnc,Laser_cutting,Pcb_designing,Three_d_printing,Rapid_proto,Web_mobile

class ServiceRepository(BaseRepository):
    def __init__(self):
        self.model = Service

class CncRepository(BaseRepository):
    def __init__(self):
        self.model = Cnc

class Laser_cuttingRepository(BaseRepository):
    def __init__(self):
        self.model = Laser_cutting

class Pcb_designingRepository(BaseRepository):
    def __init__(self):
        self.model = Pcb_designing

class Three_d_printingRepository(BaseRepository):
    def __init__(self):
        self.model = Service

class Rapid_prototypingRepository(BaseRepository):
    def __init__(self):
        self.model = Rapid_proto

class Web_mobileRepository(BaseRepository):
    def __init__(self):
        self.model = Web_mobile
