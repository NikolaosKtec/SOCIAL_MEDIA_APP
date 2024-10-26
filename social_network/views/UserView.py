
from django.contrib.auth import get_user_model
# caching ...
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from ..serializers import UserSerializer

queryset = get_user_model()


# fetch Users an create Users
class Pagination(PageNumberPagination):
    page_size=5
    page_size_query_param=page_size
    max_page_size=100

class UserView(APIView,PageNumberPagination):
    pagination_class = Pagination  
    permission_classes = [IsAuthenticated]
    # with auth
    @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
    def get(self,request,*args, **kwargs):
        
            paginator = self.pagination_class()

            page = paginator.paginate_queryset(queryset.objects.all(), request)
            page = UserSerializer(page,many=True).data
            # return Response('ok')
            return Response( data={'data':page,'next':paginator.get_next_link(),'previous':paginator.get_previous_link()})
    
    
    def post(self, request,*args, **kwargs):

        serializer = UserSerializer(data=request.data, many=True, allow_empty=False)
        if serializer.is_valid():

            # serializer.make_password()
        
           
            serializer.save()

            return Response(data='created',status=status.HTTP_201_CREATED)
        else:
            return Response(data={'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)  
        
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    # with auth
    @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
    def get(self,request,id,*args, **kwargs):

        if queryset.objects.filter(id=id).first() is None:
            return Response('error, user does not exist',status=status.HTTP_400_BAD_REQUEST)
        elif request.user.id == id:
            return Response('error, user does not same',status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        # admitindo que este id de user existe...
        user.addFollowers(id)
        
        serializer = UserSerializer(data=user)
        serializer.is_valid()
        serializer.update(user,serializer._validated_data)
        
        return Response({'created':f'now user{user.username} follows user_id:{id}'},status=status.HTTP_201_CREATED)
       

class UnfollowView(APIView):
   permission_classes = [IsAuthenticated]
   @method_decorator(cache_page(60 * 15 ),vary_on_headers("Authorization")) #15 minutes
   def get(self,request,id,*args, **kwargs):

        if queryset.objects.filter(id=id).first() is None:
            return Response('error, user does not exist',status=status.HTTP_400_BAD_REQUEST)
        elif request.user.id == id:
            return Response('error, user does not same',status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        # admitindo que este id de user existe...
        user.removeFollowers(id)
        
        serializer = UserSerializer(data=user)
        serializer.is_valid()
        serializer.update(user,serializer._validated_data)
        
        return Response({'created':f'now user{user.username} unfollows user_id:{id}'},status=status.HTTP_201_CREATED)
       