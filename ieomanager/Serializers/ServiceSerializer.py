from ieomanager.models import Service,Cnc,Laser_cutting,Pcb_designing,Three_d_printing,Rapid_proto,Web_mobile
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_polymorphic.serializers import PolymorphicSerializer

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class CncSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cnc
        fields = '__all__'

class Laser_cuttingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laser_cutting
        fields = '__all__'

class Pcb_designingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pcb_designing
        fields = '__all__'

class Three_d_printingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Three_d_printing
        fields = '__all__'

# class Rapid_prototypingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rapid_prototyping
#         fields = '__all__'

class Web_mobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Web_mobile
        fields = '__all__'

class ServicePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Service: ServiceSerializer,
        Cnc: CncSerializer,
        Laser_cutting: Laser_cuttingSerializer,
        Pcb_designing: Pcb_designingSerializer,
        Three_d_printing: Three_d_printingSerializer,
        # Rapid_prototyping: Rapid_prototypingSerializer,
        Web_mobile: Web_mobileSerializer,
    }
