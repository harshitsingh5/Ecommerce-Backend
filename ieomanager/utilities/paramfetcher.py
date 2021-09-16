from excess_admin.middleware import ParamMissingHandler

class GetFromGet:
    def __init__(self,request):
        self.request=request
        self.value=None
        self.key=None

    def getValue(self,key):
        self.key=key
        try:
            self.value=self.request.GET.get(key)
            return self.value
        except Exception as e:
            raise ParamMissingHandler

class GetFromPost:    
    def __init__(self,request):
        self.request=request
        self.value=None
        self.key=None

    def getValue(self,key):
        self.key=key
        try:
            self.value=self.request.POST.get(key)
            return self.value
        except Exception as e:
            raise ParamMissingHandler



class GetFromJson:
    def __init__(self,request):
        self.request=request
        self.value=None
        self.key=None

    def getValue(self,key):
        self.key=key
        try:
            import json
            json_data=json.loads(self.request.body)
            self.value=json_data[key]
            return self.value
        except Exception as e:
            raise ParamMissingHandler


class GetFromHeader:
    def __init__(self,request):
        self.request=request
        self.value=None
        self.key=None
    def getValue(self,key):
        self.key=key
        try:
            self.value=self.request.META[self.key]
            return self.value
        except Exception as e:
            raise ParamMissingHandler
    