from typing import Any
from django.shortcuts import render
from django.views import View
from . import models
from django.http import JsonResponse
from django.core.serializers import serialize

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import json
from icecream import ic

class SalesListView(View):
    def __init__(self, *args, **kwargs):
        self.bookings = models.Booking.objects.all()
        self.customers = models.Customer.objects.all()
        self.context = {
            "customers": self.customers
        }

    def get(self, request, *args, **kwargs):
        id = request.GET.get('booking', None)
        if(id is not None):
            get_booking = models.Booking.objects.filter(id=id)
            if(get_booking):
                return JsonResponse(list(get_booking.values()),safe=False)
            else:
                return JsonResponse({"satus":400,"error":"Booking not found"}, status=400)
        
        self.context['bookings'] = self.bookings

        return render(request, 'Admin/sales-list.html', context=self.context,status=200)
    

class Booking(View):
    def post(self, request, *args, **kwargs):
        customer_id = request.POST.get('customer_id', None)
        shop = request.POST.get('shop', None)
        monthly_rent = request.POST.get('monthly_rent', None)
        advance_payment = request.POST.get('advance_payment', None)
        advance_payment_date = request.POST.get('advance_payment_date', None)
        rent_start_date = request.POST.get('rent_start_date', None)

        context = {}

        try:
            if customer_id and shop and monthly_rent and advance_payment and rent_start_date:
                rent_date = datetime.strptime(rent_start_date,"%d-%m-%Y")
                advance_pay_date = datetime.strptime(advance_payment_date,"%d-%m-%Y") if advance_payment_date != '' else None

                # convert into proper format
                advance_pay_date = advance_pay_date.strftime("%Y-%m-%d") if advance_payment_date != '' else None
                rent_date = rent_date.strftime("%Y-%m-%d")

                customer = models.Customer.objects.get(id=customer_id)
                booking = models.Booking.objects.create(
                    customer = customer,
                    shop = shop,
                    monthly_rent = float(monthly_rent),
                    advance_payment = float(advance_payment),
                    rent_start_date = rent_date,
                    advance_payment_date = advance_pay_date
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
        
    def put(self,request):
        body = json.loads(request.body.decode('utf-8'))
        
        booking_id = body.get('booking_id',None)
        advance_payment = body.get('advance_pay',None)
        advance_payment_date = body.get('advance_payment_date',None)
        end_date = body.get('end_date',None)
        is_ended = False if body.get('is_ended') else True
        last_payment_date = body.get('last_pay',None)
        monthly_rent = body.get('monthly_rent',None)
        rent_start_date = body.get('start_date',None)
        total_paid = body.get('total_paid',None)

        try:
            if (booking_id and advance_payment 
                    and monthly_rent and 
                    total_paid and rent_start_date):
                booking = models.Booking.objects.filter(id=booking_id).first()

                if (booking is None):
                    context = {
                        "status": 400,
                        "message": "Booking not found"
                    }
                    return JsonResponse(context,status=400)
                
                

                # formate date
                start_date = datetime.strptime(rent_start_date,"%d-%m-%Y")
                start_date = start_date.strftime("%Y-%m-%d")
                advance_date = datetime.strptime(advance_payment_date,"%d-%m-%Y") if advance_payment_date else None
                advance_date = advance_date.strftime("%Y-%m-%d") if advance_date else None
                pay_date = datetime.strptime(last_payment_date,"%d-%m-%Y") if last_payment_date else None
                pay_date = pay_date.strftime("%Y-%m-%d") if pay_date else None
                rent_end_date = datetime.strptime(end_date, "%d-%m-%Y") if end_date else None
                rent_end_date = rent_end_date.strftime("%Y-%m-%d") if rent_end_date else None
                
                booking.advance_payment = advance_payment
                booking.monthly_rent = monthly_rent
                booking.total_paid = total_paid
                booking.rent_start_date = start_date
                booking.advance_payment_date = advance_date
                booking.last_payment_date = pay_date
                booking.is_ended = True if is_ended else False
                booking.end_date = rent_end_date if rent_end_date and is_ended else None

                ic(end_date, rent_end_date, is_ended)
                if (is_ended and rent_end_date is None) or (rent_end_date and is_ended is False):
                    context= {
                        "status": 400,
                        "message": "Required end date and must be inactivated"
                    }
                    return JsonResponse(context,status=400)

                booking.save()

                context = {
                    "status": 200,
                    "message": "Booking Successfully Updated"
                }

                return JsonResponse(context,status=200)
            else:
                context = {
                    "status":400,
                    "message": "Missing required fields"
                }
                return JsonResponse(context,status=400)
            
        except Exception as e:
            
            context = {
                    "status":501,
                    "message": "Internal Server Error",
                    "error": str(e)
                }
            ic(context)
            return JsonResponse(context,status=501)
        
        

class MakePayment(View):
    def __init__(self) -> None:
        self.context = {}

    def count_months(self, **months):
        ic(months)
        count = 0
        selected_months = []

        for key, value in months.items():
            if value is not None:
                count += 1
                selected_months.append(key)
        
        return count, selected_months

    def post(self,request, *args, **kwargs):
        booking_id = request.POST.get('booking_id', None)
        amount = request.POST.get('amount', None)
        payment_date = request.POST.get('payment_date', None)

        # months
        january = request.POST.get('jan', None)
        february = request.POST.get('feb', None)
        march = request.POST.get('mar', None)
        april = request.POST.get('apr', None)
        may = request.POST.get('may', None)
        june = request.POST.get('jun', None)
        july = request.POST.get('jul', None)
        august = request.POST.get('aug', None)
        september = request.POST.get('sep', None)
        october = request.POST.get('oct', None)
        november = request.POST.get('nov', None)
        december = request.POST.get('dec', None)


        try:
            if booking_id and amount and payment_date:
                total_months, selected_months = self.count_months(
                    january = january, february = february, march = march, april = april,
                    may = may,june = june,july=july,august=august,
                    september=september,october=october,november=november,december=december
                )

                if total_months == 0:
                    self.context['status'] = 400
                    self.context['message'] = 'Please select a month'
                    return JsonResponse(self.context, status=400)

                booking = models.Booking.objects.get(id=booking_id)

                if not booking:
                    self.context['status'] = 400
                    self.context['message'] = 'Invalid booking information'
                    return JsonResponse(self.context, status=400)
                
                amount = float(amount)
                monthly_payment = amount / total_months

                # convert date to proper format
                date = datetime.strptime(payment_date,"%d-%m-%Y")
                date = date.strftime("%Y-%m-%d")

                for month in selected_months:
                    models.MonthlyPayment.objects.create(
                        booking = booking,
                        date = date,
                        month = month,
                        amount = monthly_payment
                    ).save()
                
                booking.last_payment_date = date
                booking.total_paid +=amount
                booking.save()

                self.context['status'] = 200
                self.context['message'] = 'Successfully created new payment.'
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
            
class PaymentDetails(View):
    def get(self, request, id):
        details = models.MonthlyPayment.objects.filter(booking_id = id).values()
        # json_details = serialize("json",details)
        return JsonResponse({'details': list(details)})

class Customer(View):
    def __init__(self) -> None:
        self.customers = models.Customer.objects.all().order_by('date_created')
        self.context = {
        }

    def get(self, request, *args, **kwargs):
        self.context["customers"] = self.customers
        return render(request, 'Admin/customer.html', context=self.context)  
    
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
