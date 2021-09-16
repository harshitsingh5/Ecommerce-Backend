from functools import wraps
from .jwtjose import JWTService
import inspect
from django.http import *
from rest_framework.response import Response
from ieomanager.models import User

AUTHORIZATION_HEADER_NAME = "HTTP_AUTHORIZATION"
BEARER_METHOD_TEXT = "Bearer "

jwt_service = JWTService()


def auth_login_required(roles):
	def login_required(decorated_function):
		@wraps(decorated_function)
		def decorator(*args, **kwargs):
			request = args[1]
			# if not isinstance(request, HttpRequest):
			# 	raise RuntimeError(
			# 		"This decorator can only work with django view methods accepting a HTTPRequest as the first parameter")

			if AUTHORIZATION_HEADER_NAME not in request.META:
				return Response({"message":"Missing authentication header"}, status=402)

			jwt_token = request.META[AUTHORIZATION_HEADER_NAME].replace(BEARER_METHOD_TEXT, "")
			# try:
			decoded_payload = jwt_service.verify_token(jwt_token)
			user_id = decoded_payload["user_id"]
			user = User.objects.get(uuid=user_id)
			role = user.get_role()

			if role not in roles:
				return Response({"message":"You don't have permission to access this resource"},  status=402)

			parameter_names = inspect.getargspec(decorated_function).args

			if "user_id" in parameter_names:
				kwargs["user_id"] = user_id

			# user_obj = type('', (), {})()
			# user_obj.o = user
			# user_obj.token=jwt_token
			request.__setattr__("user", user)
			request.__setattr__("token", jwt_token)

			return decorated_function(*args, **kwargs)
			# except:
			# 	return Response({"message":"Incorrect or expired authentication header"}, status=402)

		return decorator

	return login_required
