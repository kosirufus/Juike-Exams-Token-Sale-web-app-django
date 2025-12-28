from rest_framework import serializers
from service_section.Serviceproduct.models import ServiceProduct
from service_section.Subject.models import Subject

CLASS_CHOICES = ['science', 'art']

class ServiceOrderCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    student_class = serializers.ChoiceField(choices=CLASS_CHOICES)
    product_ids = serializers.ListField(
        child=serializers.IntegerField(), min_length=1
    )
    subject_ids = serializers.ListField(
        child=serializers.IntegerField(), min_length=9, max_length=9
    )

    def validate(self, data):
        products = ServiceProduct.objects.filter(
            id__in=data['product_ids'],
            is_active=True
        )
        if products.count() != len(data['product_ids']):
            invalid_ids = set(data['product_ids']) - set(products.values_list('id', flat=True))
            raise serializers.ValidationError(f"Invalid product IDs: {invalid_ids}")

        subjects = Subject.objects.filter(id__in=data['subject_ids'])
        if subjects.count() != 9:
            invalid_ids = set(data['subject_ids']) - set(subjects.values_list('id', flat=True))
            raise serializers.ValidationError(f"Invalid subject IDs: {invalid_ids}")

        return data
