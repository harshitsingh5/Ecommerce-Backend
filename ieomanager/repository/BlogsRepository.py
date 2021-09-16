from .baseRepository import BaseRepository
from ieomanager.models import Blogs, Comments, Replies

class BlogsRepository(BaseRepository):
    def __init__(self):
        self.model = Blogs

class CommentsRepository(BaseRepository):
    def __init__(self):
        self.model = Comments

class RepliesRepository(BaseRepository):
    def __init__(self):
        self.model = Replies
