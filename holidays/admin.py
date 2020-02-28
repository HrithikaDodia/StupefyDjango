from django.contrib import admin
from .models import Place,BookingPlace,Book,PlaceImage,Flight,FlightPerson,FlightBooking
# Register your models here.

admin.site.register(Place)
admin.site.register(BookingPlace)
admin.site.register(Book)
admin.site.register(PlaceImage)
admin.site.register(Flight)
admin.site.register(FlightPerson)
admin.site.register(FlightBooking)