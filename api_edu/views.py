from rest_framework import generics, permissions
from app_edu import models
from api_edu import serializers


class CategoryList(generics.ListCreateAPIView):
    """ List/Create Views for /categories extend ListCreateAPIView """
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    """ Get, Update, Detele Views for /category/pk
        extend RetrieveUpdateDestroyAPIView 
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class PostList(generics.ListCreateAPIView):
    """ List/Create Views for / extend ListCreateAPIView """
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostDetails(generics.ListCreateAPIView):
    """ Get, Update, Detele Views for /post/pk
        extend RetrieveUpdateDestroyAPIView 
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
