from rest_framework.serializers import ModelSerializer

from holidays.models import Place

class PlaceListSerializer(ModelSerializer):
    class Meta:
        model=Place
        fields=[
            'package',
            'name1',
            'name2',
            'name3',
            'slug',
            'price',
            'discount_price',
        ]

class PlaceDetailSerializer(ModelSerializer):
    class Meta:
        model=Place
        fields=[
            'package',
            'name1',
            'name2',
            'name3',
            'slug',
            'description',
            'price',
            'discount_price',
        ]

class PlaceUpdateSerializer(ModelSerializer):
    class Meta:
        model=Place
        fields=[
            'description',
            'price',
            'discount_price',
        ]