from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
# from rest_framework.authtoken.models import Token
# from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from ieomanager.Serializers import BlogsSerializer,BlogsEditSerializer,CommentsSerializer,RepliesSerializer
# from ieomanager.models import Blogs, Comments, Replies
from ieomanager.repository import BlogsRepository, CommentsRepository, RepliesRepository
# from datetime import datetime,timedelta
from django.utils import timezone
from ieomanager.permisions import IsAdminOrOwner
from functools import partial
from ieomanager.utilities import auth_login_required

class BlogsList(APIView):
	br=BlogsRepository()
	def get_permission(self,request):
		if request.method=="GET":
			return [AllowAny]
		elif request.method == "POST":
			return [IsAdminOrOwner]
		else:
			return [IsAuthenticated]

	def get(self,request):
		blogs = self.br.GetAll()
		serializer = BlogsSerializer(blogs, many=True)
		return Response(serializer.data)


	@auth_login_required(['admin'])
	def post(self, request, *args, **kwargs):
		user=request.user
		heading = request.data['heading']
		slug='-'
		slug=slug.join(heading.split('-'))
		serializer = BlogsSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		blog = self.br.Create(values={'user':user,
									  'heading':serializer.validated_data['heading'],
									  'slug':slug,
									  'thumbnail': serializer.validated_data['thumbnail'],
									  'html_data':serializer.validated_data['html_data']
									  })
		serializer = BlogsSerializer(blog)
		return Response(serializer.data, status=201)


class Blog_details(APIView):
	br=BlogsRepository()
	cr=CommentsRepository()
	def get(self,request,slug):
		blog = self.br.GetFirst(filters=[('slug',slug)])
		blog_serializer = BlogsSerializer(blog)
		comments = blog.comments.all()
		comments_serializer = CommentsSerializer(comments, many=True)
		if blog_serializer.data['heading'] and blog_serializer.data['slug']:
			return Response({"data":{"blog":blog_serializer.data, "comments":comments_serializer.data}},status=200)
		return Response({"msg":"Blog not found"}, status=400)

	@auth_login_required(['admin'])
	def put(self, request, slug):
		blog = self.br.GetFirst(filters=[('slug',slug)])
		serializer = BlogsEditSerializer(blog,data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['heading'] and serializer.validated_data['slug']:
			blog = serializer.save()
			serializer = BlogsEditSerializer(blog)
			return Response({"msg":"Blog Updated","blog_details":serializer.data}, status=201)
		return Response({"msg":"Invalid Data"}, status=400)

	#delete a blog
	@auth_login_required(['admin'])
	def delete(self, request, slug):
		blog = self.br.GetFirst(filters=[('slug',slug)])
		if not blog:
			return Response({"msg":"blog not found"}, status=400)
		blog.delete()
		return Response({"msg":"Blog deleted"}, status=201)


class Blog_add_comment(APIView):
	permission_classes = [AllowAny]
	br=BlogsRepository()
	cr=CommentsRepository()
	@auth_login_required(['user','admin'])
	def post(self, request, blog_uuid):
		user = request.user
		blog = self.br.GetFirst(filters=[('uuid',blog_uuid)])
		if not blog:
			return Response({"msg":"No Such Blog Found"},status=400)
		cs = CommentsSerializer(data=request.data)
		cs.is_valid(raise_exception=True)
		x = cs.validated_data
		comment = self.cr.Create(values={'user':user,"comment_data":x['comment_data']})
		blog.comments.add(comment)
		cs = CommentsSerializer(comment)
		return Response({"msg":"Comment Added","comment":cs.data}, status=201)


class View_replies(APIView):
	permission_classes = [AllowAny]
	cr=CommentsRepository()
	def get(self,request,blog_uuid,comment_uuid):
		replies = self.cr.GetFirst(filters=[('uuid',comment_uuid)]).replies.all()
		replies = RepliesSerializer.setup_eager_loading(replies)
		replies_serializer = RepliesSerializer(replies, many=True)
		return Response(replies_serializer.data)


class Add_reply(APIView):
	cr=CommentsRepository()
	rr=RepliesRepository()
	@auth_login_required(['user','admin'])
	def post(self,request,comment_uuid):
		comment = self.cr.GetFirst(filters=[('uuid',comment_uuid)])
		if not comment:
			return Response({"msg":"No Such Comment Found"},status=400)
		rs = RepliesSerializer(data=request.data)
		rs.is_valid(raise_exception=True)
		x = rs.validated_data
		reply = self.rr.Create(values={"reply_data":x['reply_data']})
		comment.replies.add(reply)
		rs = RepliesSerializer(reply)
		return Response({"msg":"Reply Added","reply":rs.data}, status=201)



class Comment_delete(APIView):
	cr=CommentsRepository()
	@auth_login_required(['admin'])
	def delete(self, request, blog_uuid, comment_uuid):
		comment = self.cr.GetFirst(filters=[('uuid',comment_uuid)])
		if not comment:
			return Response({"msg":"Comment not found"}, status=400)
		comment.delete()
		return Response({"msg":"Comment deleted"}, status=201)


class Reply_delete(APIView):
	rr=RepliesRepository()
	@auth_login_required(['admin'])
	def delete(self, request, blog_uuid, comment_uuid, reply_uuid):
		reply = self.rr.GetFirst(filters=[('uuid',reply_uuid)])
		if not reply:
			return Response({"msg":"Reply not found"}, status=400)
		reply.delete()
		return Response({"msg":"Reply deleted"}, status=201)






#
