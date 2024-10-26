# from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated

from ..models import PostModel
querrytset = PostModel()


from ..serializers import PostModelSerializer
# from ..serializers import UserSerializer

# fetch Users an create Users
class Pagination(PageNumberPagination):
    page_size=5
    page_size_query_param=page_size
    max_page_size=100

class PostView(APIView,PageNumberPagination):
    
    pagination_class = Pagination()
    permission_classes = [IsAuthenticated]
    @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
    def get(self,request):
        paginator = self.pagination_class
        # user = 
        
        page = paginator.paginate_queryset(querrytset.objects.all(), request)
        page = PostModelSerializer(page,many=True).data
        return Response(data={'data':page,'next':paginator.get_next_link(),'previous':paginator.get_previous_link()})

    def post(self,request,*args, **kwargs):
        
        serializer = PostModelSerializer(data=request.data, many=True,allow_empty=False)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
class LikePost(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
    def patch(self,request,id):
        post = PostModel.objects.filter(id=id).first()

        if post in None:
                    return Response('error, post does not exist',status=status.HTTP_400_BAD_REQUEST)
        
        post.addLike()
        serializer = PostModelSerializer(data=post, many=False,allow_empty=False)
        serializer.is_valid()
        serializer.update(post,serializer._validated_data)
        return Response("Post has ben liked")
    
class FeedView(APIView,PageNumberPagination):
        pagination_class = Pagination()
        permission_classes = [IsAuthenticated]
        
        @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
        def get(self,request):
                followers = request.user.getFollowersList()
                
                paginator = self.pagination_class
                posts = []
                # empty cases
                if not followers:
                    return Response(followers)
                
                # for item in followers:
                #     posts.append(querrytset.objects.filter(user=int(item))
                #                  .first())


                page = paginator.paginate_queryset(querrytset.objects
                                                   .filter(user_fk=followers).first().order_by('wasCreated'), request)
                page = PostModelSerializer(page,many=True).data
            
                return Response( data={'data':page,'next':paginator.get_next_link(),'previous':paginator.get_previous_link()})
  



