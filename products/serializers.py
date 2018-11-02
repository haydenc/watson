from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from products.models import Product, ProductComment
from watson.models import WatsonAnalysisResults


class ProductCommentSerializer(serializers.ModelSerializer):
    primary_emotion = serializers.SerializerMethodField()

    @staticmethod
    def get_primary_emotion(comment_instance):
        # Slightly flaky here - don't like the lack of 1-1 enforcement on the generic foreign key
        comment_content_type = ContentType.objects.get_for_model(ProductComment)
        watson_analysis = WatsonAnalysisResults.objects\
            .filter(job__object_id=comment_instance.id, job__content_type=comment_content_type)\
            .first()
        if watson_analysis:
            return watson_analysis.get_primary_emotion()

    class Meta:
        model = ProductComment
        fields = ("id", "comment", "primary_emotion")


class ProductSerializer(serializers.ModelSerializer):
    comments = ProductCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ("id", "sku", "name", "comments")
