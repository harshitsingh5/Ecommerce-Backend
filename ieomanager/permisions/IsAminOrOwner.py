from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    def __init__(self, user=None):
        super().__init__()
        self.user = user
    def has_permission(self,request,view):
        message = "You are Not Allowed To access this content"
        if request.user.admin.first()!=None:
            return True
        if request.user == self.user:
            return True
        else:
            False