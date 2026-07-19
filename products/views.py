#from itertools import product
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from orders import models
from .models import Collection, Product
from rest_framework import status
from .serilaizer import CollectionSerializer, ProductSerializer

class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     #for printing the validated data, you can use serializer.validated_data
    #     #serializer.validated_data
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({"error": "Product cannot be deleted because it is associated with orders."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_200_OK)
    

@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be deleted because it includes one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)