import math
class Pagenitions:
    def __init__(self,posts,limit=5,page=1):
        self.limit=limit
        self.page=page
        self.posts=posts
    
    def GetPosts(self):
        if self.limit<1:
            self.limit=10
        if self.page<1:
            self.page=1
        pages=self.GetPages()
        self.posts=self.posts[self.limit*(self.page-1):self.limit*self.page]
        self.count=len(self.posts)
        result={'count':self.count,"pages":pages,"posts":self.posts,"offset":self.GetOffset(),"current_page":self.page}
        return result
    
    def GetPages(self):
        total=int(math.ceil(len(self.posts)/float(self.limit)))
        pages=[x for x in range(1,total+1)]
        return pages
    
    def GetOffset(self):
        offset=self.limit*(self.page-1)+1
        return offset