from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Place(models.Model):
    name1 = models.CharField(max_length = 150)
    country_name1 = models.CharField(max_length = 150, default = 'India')
    name2 = models.CharField(max_length = 150,blank=True)
    country_name2 = models.CharField(max_length = 150, default = 'India',blank=True)
    name3 = models.CharField(max_length = 150,blank=True)
    country_name3 = models.CharField(max_length = 150, default = 'India',blank=True)
    package = models.CharField(max_length = 150)
    description = models.TextField(blank = True)
    slug = models.SlugField(max_length = 250,blank = True)
    price = models.DecimalField(max_digits = 10,decimal_places = 2,null=True)
    discount_price = models.DecimalField(max_digits = 10,decimal_places = 2,null=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.package)
        super(Place, self).save(*args, **kwargs)

    def __str__(self):
        return self.package

    def get_absolute_url(self):
        return reverse("holidays:detail", kwargs={"slug": self.slug}) 

    def get_add_to_cart_url(self):
        return reverse("holidays:add-to-cart", kwargs={"slug": self.slug})
    
    def get_increase_url(self):
        return reverse("holidays:increase", kwargs={"slug": self.slug})
    
    def get_reduce_num_url(self):
        return reverse("holidays:reduce-num", kwargs={"slug": self.slug})
    
    def get_remove_from_cart_url(self):
        return reverse("holidays:remove-from-cart", kwargs={"slug": self.slug})

    class Meta:
        ordering = ['-id']

class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete = 'models.CASCADE')
    image = models.ImageField(upload_to = 'images')

class BookingPlace(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    package = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place')
    booked = models.BooleanField(default=False)
    number = models.IntegerField(default=1)
    def __str__(self):
        return str(self.package)
    
    def get_total_place_price(self):
        return self.number*self.package.price
    
    def get_total_place_discount_price(self):
        return self.number*self.package.discount_price

class Flight(models.Model):
    name = models.CharField(max_length = 250)
    company_name = models.CharField(max_length = 250)
    source = models.CharField(max_length = 120) 
    destination = models.CharField(max_length = 120)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length = 250,blank = True, default=None)
    price = models.DecimalField(max_digits = 10,decimal_places = 2,null=True)
    discount_price = models.DecimalField(max_digits = 10,decimal_places = 2,null=True)
    destination_code = models.CharField(max_length=3)
    source_code=models.CharField(max_length=3)
    date = models.DateField(blank=True, null=True)
    dept_time = models.TimeField()
    arrival = models.TimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Flight, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("holidays:flight_detail", kwargs={"slug": self.slug}) 

class FlightBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete = models.DO_NOTHING, related_name='flight')
    date = models.DateTimeField(auto_now = True)

class FlightPerson(models.Model):
    flightbooking = models.ForeignKey(FlightBooking, on_delete=models.DO_NOTHING, related_name='flight_booking')
    firstname = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    row_no = models.CharField(max_length = 1, default=None)
    seat_no = models.IntegerField()
    booked = models.BooleanField(default=False)
    class Meta:
        unique_together = ('seat_no', 'row_no')

    def get_flight_remove_from_cart_url(self):
        return reverse("holidays:flight_remove_from_cart", kwargs={"id": self.id})

class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    packages = models.ManyToManyField(BookingPlace)
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.user)
