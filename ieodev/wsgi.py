python_home = '/home/ubuntu/ieoenv'
import os
import sys
sys.path.append('/home/ubuntu/Ecommerce - Backend')
sys.path.append('/home/ubuntu/Ecommerce - Backend/ieodev')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ieodev.settings')

application = get_wsgi_application()
