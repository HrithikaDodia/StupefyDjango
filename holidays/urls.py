from django.urls import path
from . import views

app_name = 'holidays'
urlpatterns = [
    path('list/',views.PlaceListView.as_view(),name='list'),
    path('detail/<slug:slug>/',views.PlaceDetailView.as_view(),name='detail'),
    path('add-to-cart/<slug:slug>/',views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/',views.remove_from_cart,name='remove-from-cart'),
    path('order-summary/',views.order_summary,name='order-summary'),
    path('payment/',views.handle_payment,name='payment'),
    path('increase/<slug:slug>',views.increase,name='increase'),
    path('reduce-num/<slug:slug>',views.reduce_num,name='reduce-num'),
    path('pdf/<int:id>/',views.GeneratePdf.as_view(),name='pdf'),
    path('order/',views.order,name='order'),
    path('flight/', views.FlightListView.as_view(),name='flight'),
    path('flight-detail/<slug:slug>/',views.FlightDetailView.as_view(),name='flight_detail'),
    path('flight-booking-create/<int:id>/',views.FlightBookingCreate.as_view(),name='flight_booking_create'),
    path('flight-booking-detail/<pk>/',views.FlightBookingDetailView.as_view(),name='flight_booking_detail'),
    path('flight-person-detail/<pk>/',views.FlightPersonDetailView.as_view(),name='flight_person_detail'),
    path('booking-complete/',views.booking_complete,name='booking_complete'),
    path('flight-remove-from-cart/<int:id>',views.flight_remove_from_cart,name='flight_remove_from_cart')
]