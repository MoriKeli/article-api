from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

# Authentication
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.models import Article
from api.serializers import ArticleSerializer


class ArticleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        
        return Response(serializer.data, )
    
    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
class ArticleDetails(APIView):
    def get_object(self, pk):
        try:
            return Article.objects.get(id=pk)
        
        except Article.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
    
    
    # request must be included in get() & put()  functions or else TypeError: <func name>() got multiple values for argument 'pk'  will be raised.
    # function put() cannot work without request.
     
    def get(self, request, pk):
        serializer = ArticleSerializer(self.get_object(pk))     # article = self.get_object(pk)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        
        return Response(status.HTTP_204_NO_CONTENT)
    

# Using generic and mixins.
class ArticleGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
    ):
    
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    
    lookup_field = 'id'
    
    # authentication_classes = [SessionAuthentication, BasicAuthentication]   # first check SessionAuthentication and then BasicAuthentication
    authentication_classes = [TokenAuthentication]  # using generated token
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    
    
    def post(self, request):
        return self.create(request)
        
    def put(self, request, id=None):
        return self.update(request, id)
    
    def delete(self, request, id):
        return self.destroy(request, id)
    
    