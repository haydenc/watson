import uuid

from django.db import models

from watson.models import WatsonAnalysisBase


class Product(models.Model):
    """Model representing a single stock item"""
    sku = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class ProductComment(WatsonAnalysisBase):
    """A single product comment"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    watson_fields = ("comment",)

    def __str__(self):
        return "Comment on {product}".format(product=self.product.name)
