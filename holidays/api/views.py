from rest_framework.generics import ListAPIView,RetrieveAPIView,UpdateAPIView

from holidays.models import Place
from .serializers import PlaceListSerializer,PlaceDetailSerializer,PlaceUpdateSerializer

class PlaceListAPIView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceListSerializer

class PlaceDetailAPIView(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceDetailSerializer
    lookup_field = 'slug'

class PlaceUpdateAPIView(UpdateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceUpdateSerializer
    lookup_field = 'slug'