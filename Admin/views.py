from typing import Any
from django.shortcuts import render
from django.views import View
from . import models
from django.http import JsonResponse

class SalesListView(View):
    def __init__(self, *args, **kwargs):
        self.bookings = models.Booking.objects.all()
        self.customers = models.Customer.objects.all()
        self.context = {
            "customers": self.customers
        }

    def get(self, request, *args, **kwargs):
        self.context['bookings'] = self.bookings

        return render(request, 'admin/sales-list.html', context=self.context,status=200)
    
class NewBooking(View):
    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id', None)
        shop = request.POST.get('shop', None)
        monthly_rent = request.POST.get('monthly_rent', None)
        advance_payment = request.POST.get('advance_payment', None)
        advance_payment_date = request.POST.get('advance_payment_date', None)
        context = {}

        try:
            if customer_id and shop and monthly_rent and advance_payment:
                customer = models.Customer.objects.get(id=customer_id)
                booking = models.Booking.objects.create(
                    customer = customer,
                    shop = shop,
                    monthly_rent = float(monthly_rent),
                    advance_payment = float(advance_payment),
                    advance_payment_date = advance_payment_date if advance_payment_date != '' else None
                )
                booking.save()

                context['status'] = 200
                context['message'] = 'Successfully created new booking.'
                return JsonResponse(context, status=200)
            else:
                context['status'] = 400
                context['message'] = 'Missing required parameters'
                return JsonResponse(context, status=400)
            
        except Exception as e:
            context['status'] = 501
            context['message'] = 'Internal Server Error'
            context['error'] = str(e)
            return JsonResponse(context, status=501)


class Customer(View):
    def __init__(self) -> None:
        self.customers = models.Customer.objects.all()
        self.context = {
        }

    def get(self, request, *args, **kwargs):
        self.context["customers"] = self.customers
        return render(request, 'admin/customer.html', context=self.context)  
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        number = request.POST.get('number', None)
        nid = request.POST.get('nid', None)
        address = request.POST.get('address', None)

        try:
            if name and number and address:
                customer = models.Customer.objects.create(
                    name=name, 
                    email=email, 
                    nid=nid, 
                    address=address, 
                    number = number
                    )
                customer.save()

                # self.context['customers'] = models.Customer.objects.all()
                self.context['status'] = 200
                self.context['message'] = 'Successfully created new customer.'
                return JsonResponse(self.context, status=200)
            else:
                self.context['status'] = 400
                self.context['message'] = 'Missing required parameters'
                return JsonResponse(self.context, status=400)
            
        except Exception as e:
            self.context['status'] = 501
            self.context['message'] = 'Internal Server Error'
            self.context['error'] = str(e)
            return JsonResponse(self.context, status=501)
        
    def put(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        number = request.POST.get('number', None)
        nid = request.POST.get('nid', None)
        address = request.POST.get('address', None)

        try:
            if id and name and number and address:
                customer = models.Customer.objects.create(
                    name=name, 
                    email=email, 
                    nid=nid, 
                    address=address, 
                    number = number
                    )
                customer.save()

                # self.context['customers'] = models.Customer.objects.all()
                self.context['status'] = 200
                self.context['message'] = 'Successfully created new customer.'
                return JsonResponse(self.context, status=200)
            else:
                self.context['status'] = 400
                self.context['message'] = 'Missing required parameters'
                return JsonResponse(self.context, status=400)
            
        except Exception as e:
            self.context['status'] = 501
            self.context['message'] = 'Internal Server Error'
            self.context['error'] = str(e)
            return JsonResponse(self.context, status=501)
