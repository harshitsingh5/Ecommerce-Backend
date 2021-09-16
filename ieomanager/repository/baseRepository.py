class BaseRepository:
    def __init__(self):
        pass

    def Create(self,values={}):
        new_obj = self.model(**values)
        new_obj.save()
        return new_obj

    def GetFirst(self,filters=[]):
        query = self.Query(filters=filters).first()
        return query

    def GetAll(self,filters=[]):
        query = self.Query(filters=filters)
        return query

    def Query(self,filters=[]):
        self.res=self.model.objects.all()
        query=self.res
        for fil in filters:
            query=self.Filters(query,fil[0],fil[1])
        return query

    def Filters(self,queryset, name, value):
        query=queryset.filter(**{name: value})
        return query
    
    def GetValueList(self,queryset,name,flat=True):
        query=queryset.values_list(name)
        return query
    
    def CheckExists(self,filters=[]):
        query=self.GetFirst(filters=filters)
        if query:
            return query
        else:
            return False
    def Objects(self):
        return self.model.objects
    
    def Destroy(self,obj):
        obj.delete()