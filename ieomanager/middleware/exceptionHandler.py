from django.contrib import messages
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from exceptions import SomethingWentWrong,MethodNotAllowed,ParamMissing,InvalidOrExpiredOtp

class ExceptionHandler(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, MethodNotAllowed):
            message = "Method Not Allowed"
            messages.error(request, message)
            return render(request,'excess_admin/Login.html')
        elif isinstance(exception, SomethingWentWrong):
            message = "Something Went Wrong"
            messages.error(request, message)
            return render(request,'excess_admin/Login.html')
        elif  isinstance(exception,ParamMissing):
            message = "Parameter Missing"
            messages.error(request, message)
            return render(request,'excess_admin/Login.html')
        elif isinstance(exception,InvalidOrExpiredOtp):
            message = "Invalid or Expired Otp"
            pass
        else:
            message = "Internal Server Error, Please Contact Admin"
            messages.error(request, message)
            return render(request,'excess_admin/Login.html')
