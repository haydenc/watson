from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product, ProductComment
from products.serializers import ProductSerializer, ProductCommentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def filter_queryset(self, queryset):
        queryset = super(ProductViewSet, self).filter_queryset(queryset)
        specified_sku = self.request.GET.get("sku", None)
        if specified_sku:
            queryset = queryset.filter(sku=specified_sku)
        return queryset


class ProductCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCommentSerializer
    queryset = ProductComment.objects.all()

    def filter_queryset(self, queryset):
        queryset = super(ProductCommentViewSet, self).filter_queryset(queryset)
        specified_sku = self.request.GET.get("sku", None)
        if specified_sku:
            queryset = queryset.filter(product__sku=specified_sku)
        return queryset
