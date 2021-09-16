import uuid
from datetime import datetime, timedelta

from django.conf import settings
from jose import jwt
from jose.constants import ALGORITHMS


class JWTService:
    JWT_SECRET = "secreat"
    JWT_EXP_DELTA_DAYS = 1

    @staticmethod
    def create_token(user_id, role):
        payload = {'user_id': user_id, 'role':role, 'exp': datetime.utcnow() + timedelta(days=JWTService.JWT_EXP_DELTA_DAYS)}
        token = jwt.encode(payload, JWTService.JWT_SECRET, ALGORITHMS.HS512)
        return token

    @staticmethod
    def verify_token(jwt_token):
        jwt_payload = jwt.decode(jwt_token, JWTService.JWT_SECRET, ALGORITHMS.HS512)

        return jwt_payload