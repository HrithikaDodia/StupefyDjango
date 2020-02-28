from django.shortcuts import render,get_object_or_404
from .models import Place,BookingPlace,Book,PlaceImage,Flight,FlightPerson,FlightBooking
from django.views.generic import ListView,DetailView
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.db import connection
from holidays.utils import render_to_pdf
from django.views.generic import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from .paytm import Checksum
from .forms import FlightPersonFormSet, FlightPersonForm, FlightBookingForm
from django.urls import reverse_lazy
from django.db import transaction


MERCHANT_KEY = ''

class GeneratePdf(View):
    def get_context_data(self, **kwargs):
        obj_id = self.kwargs['id']
        return obj_id

    def get(self, request, *args, **kwargs):
        obj_id = self.get_context_data()
        order = BookingPlace.objects.get(id=obj_id)
        pdf = render_to_pdf('pdf/invoice.html', {'order':order,'request':request})
        return HttpResponse(pdf, content_type='application/pdf')

def index(request):
    return render(request,'holidays/base.html',{})

class PlaceListView(ListView):
    model = Place
    template_name = 'holidays/place_list.html'
    paginate_by = 5
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            return Place.objects.filter(Q(name1__icontains=query)|Q(name2__icontains=query)|Q(name3__icontains=query)|Q(package__icontains=query))
        else:
            return Place.objects.all()
            
class PlaceDetailView(DetailView):
    model = Place
    slug_field = 'slug'
    template_name = 'holidays/place_detail.html'
    context_object_name = 'detail'
    
    
def add_to_cart(request, slug):
    package = get_object_or_404(Place, slug=slug)
    book = BookingPlace.objects.filter(package = package, 
                                    user = request.user, booked = False) 
    if not(book.exists()):
        booking_place, created = BookingPlace.objects.get_or_create(package=package, 
                                    user = request.user, booked = False)
        book = Book.objects.create(user = request.user)
        book.packages.add(booking_place)
    return redirect("holidays:detail",slug = slug)
    
    # else:
    #     booking_place = BookingPlace.objects.get_object_or_404(package=package, 
    #                                 user=request.user, booked = False)
    #     booking_place.number += 1
    #     booking_place.save()
    #     return redirect("holidays:detail",slug=slug)

   
def remove_from_cart(request, slug):
    package = get_object_or_404(Place, slug=slug)
    book = BookingPlace.objects.filter(user=request.user, booked=False,package=package)
    if book.exists():
        book.delete()
        return redirect("holidays:order-summary")
    else:
        return redirect("holidays:order-summary")

def flight_remove_from_cart(request, id):
    flight = get_object_or_404(FlightPerson, id=id)
    if flight:
        flight.delete()
        return redirect("holidays:order-summary")
    else:
        return redirect("holidays:order-summary")

def increase(request,slug):
    package = get_object_or_404(Place, slug=slug)
    book = BookingPlace.objects.get(user=request.user,booked=False,package=package)
    if book:
        book.number += 1
        book.save()
        return redirect("holidays:order-summary")

def reduce_num(request,slug):
    package = get_object_or_404(Place, slug=slug)
    book = BookingPlace.objects.get(user=request.user,booked=False,package=package)
    if book:
        book.number -= 1
        book.save()
        return redirect("holidays:order-summary")
    
def order_summary(request):
    order = BookingPlace.objects.filter(user=request.user)
    flightbooking = FlightBooking.objects.filter(user=request.user)
    return render(request,'holidays/order_summary.html',{'order': order, 'flightbooking': flightbooking})
    
def order(request):
    obj = BookingPlace.objects.filter(user=request.user, booked=False)
    flightperson = FlightPerson.objects.filter(flightbooking__user=request.user, booked=False)
    famt = 0
    for f in flightperson:
        discount_price = f.flightbooking.flight.discount_price
        price = f.flightbooking.flight.price
        if discount_price:
            famt += discount_price
        else:
            famt += price
    total_amt = 0
    for place in obj:
        if place.package.discount_price:
            tp = int(place.get_total_place_discount_price())
            total_amt = total_amt + tp
        else:
            tp = int(place.get_total_place_price())
            total_amt = total_amt + tp
    t = total_amt+famt
    ttl_amt = '%.2f' %  t
    print(ttl_amt)
    if obj.exists():
        order_id = obj[0].id
    else:
        order_id = flightperson[0].id
    param_dict = {
        "MID": "eEIZxa21528202105928",
        "ORDER_ID": str(order_id),
        "CUST_ID": str(request.user.id),
        "TXN_AMOUNT": str(ttl_amt),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "abc",
        "CALLBACK_URL": "http://127.0.0.1:8000/holidays/payment/",
    }
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
    print(param_dict)
    print(request)
    return render(request,'holidays/paytm.html',{'param_dict': param_dict})

@csrf_exempt
def handle_payment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        order_id = response_dict['ORDERID']
        book = BookingPlace.objects.get(id=order_id)
        obj = book.user
        book1 = BookingPlace.objects.filter(user=obj)
        for b in book1:
            b.booked = True
            b.save()
        flightperson = FlightPerson.objects.filter(flightbooking__user=obj)
        print(flightperson)
        for fp in flightperson:
            fp.booked = True
            fp.save()
        return render(request,"holidays/bookingcomplete.html",{"book1":book1, "flightperson":flightperson})
    else:
        return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

class FlightListView(ListView):
    model = Flight
    template_name = 'holidays/flight_list.html'
    paginate_by = 5
    def get_queryset(self):
        query1 = self.request.GET.get('q1', None)
        query2 = self.request.GET.get('q2', None)
        if query1:
            return Flight.objects.filter(Q(source__icontains=query1)&Q(destination__icontains=query2))
        else:
            return Flight.objects.all()


class FlightDetailView(DetailView):
    model = Flight
    slug_field = 'slug'
    template_name = 'holidays/flight_detail.html'
    context_object_name = 'detail'

class FlightBookingDetailView(DetailView):
    model = FlightBooking
    template_name = 'holidays/flight_booking_detail.html'
    context_object_name = 'detail'

class FlightPersonDetailView(DetailView):
    model = FlightPerson
    template_name = 'holidays/flightperson_detail.html'
    context_object_name = 'detail'

class FlightBookingCreate(CreateView):
    model = FlightBooking
    template_name = 'holidays/flight_booking_create.html'
    form_class = FlightBookingForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(FlightBookingCreate, self).get_context_data(**kwargs)
        flight_id = self.kwargs['id']
        if self.request.POST:
            data['titles'] = FlightPersonFormSet(self.request.POST)
        else:
            data['titles'] = FlightPersonFormSet()
        data['flight_id'] = flight_id
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        flight_id = context['flight_id']
        print(context)
        titles = context['titles']
        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.flight = Flight.objects.get(id=flight_id)
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(FlightBookingCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('holidays:flight_booking_detail', kwargs={'pk': self.object.pk})


def booking_complete(request):
    order = BookingPlace.objects.filter(user=request.user)
    flightbooking = FlightBooking.objects.filter(user=request.user)
    return render(request,'holidays/booking_complete.html',{'order':order,'flightbooking':flightbooking})
