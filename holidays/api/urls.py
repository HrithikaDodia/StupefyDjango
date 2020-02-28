from django.urls import path

from .views import (
    PlaceListAPIView,
    PlaceDetailAPIView,
    PlaceUpdateAPIView,
)

urlpatterns=[
    path('',PlaceListAPIView.as_view(),name='list'),
    path('<slug:slug>/detail',PlaceDetailAPIView.as_view(),name='detail'),
    path('<slug:slug>/update',PlaceUpdateAPIView.as_view(),name='update'),
]