from typing import Any
from django.shortcuts import render, redirect
from django.views import View
from . import models
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import json
from icecream import ic
import csv, io
import traceback

class Logout(LoginRequiredMixin,View):
    def __init__(self, **kwargs):
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

    def get(self, request):
        logout(request)
        return redirect(reverse('admin:login'))
    
class SalesListView(LoginRequiredMixin,View):
    def __init__(self, *args, **kwargs):
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

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
    

class Booking(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

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
        
class ImportBooking(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

    def post(self, request):
        file = request.FILES.get("file",None)

        ic(request.POST, request.FILES)
        if file is None:
            context = {
                    "status":400,
                    "message": "Missing required fields"
                }
            return JsonResponse(context,status=400)
        
        file_name = file.name
        file_ext = file_name.split(".")[-1]
        
        if file_ext != "csv":
            context = {
                    "status":400,
                    "message": "Invalid file type. Please upload a CSV file."
                }
            return JsonResponse(context,status=400)
        
        try:
            decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
            csv_dict = csv.DictReader(decoded_file, delimiter=',', quotechar='"')
            

            # Validate headers
            expected_headers = ['Shop','Name','Customer','Advance','Monthly_Rent','January','February','March','April','May',
                    'June','July','August','September','October','November','December','Start','End','Advance_Date'
                    ]
            all_months = ['January','February','March','April','May','June','July','August','September','October','November','December']
            
            if not set(expected_headers).issubset(csv_dict.fieldnames):
                 # Check for missing and unexpected headers
                missing_headers = [header for header in expected_headers if header not in csv_dict.fieldnames]

                context ={
                    "status": 400,
                    "message": "CSV headers are invalid. Missing headers: " + ", ".join(missing_headers)
                }
                return JsonResponse(context, status=400)
            
            # extrar data
            for row in csv_dict:
                shop = row.get('Shop', "--")
                name = row.get('Name', None)
                customer_no = row.get('Customer', None)
                advance = row.get('Advance', 0)
                monthly_rent = row.get('Monthly_Rent', 0)
                paid_months = {month:row.get(month,None) for month in all_months if row.get(month,None)}
                rent_start_date = row.get('Start', "01-01-1001")
                end = row.get('End', None)
                advance_date = row.get('Advance_Date', None)

                # ic(shop,name,customer_no,advance,monthly_rent,paid_months,rent_start_date,end,advance_date)

                if name and monthly_rent :

                    customer = None
                    if customer_no != '' and customer_no == '2':
                        ic(customer_no)
                        customer = models.Customer.objects.filter(name=name).first()
                        ic(customer,"customer 1")
                    
                    if customer is None:
                        customer = models.Customer.objects.create(
                            name=name,
                            number= "no number",
                            address = "no address",
                        )
                    # ic(customer,"Customer 2")
                    
                    # ic(customer)
                    shops = shop.split(",")
                    # ic(name,shop,advance,advance_date,monthly_rent,rent_start_date,paid_months)
                    for s in shops:
                        # formate date
                        start_date = datetime.strptime(rent_start_date,"%d-%m-%Y")
                        start_date = start_date.strftime("%Y-%m-%d")
                        advance_payment_date = datetime.strptime(advance_date,"%d-%m-%Y") if advance_date else None
                        advance_payment_date = advance_payment_date.strftime("%Y-%m-%d") if advance_payment_date else None
                        rent_end_date = datetime.strptime(end, "%d-%m-%Y") if end else None
                        rent_end_date = rent_end_date.strftime("%Y-%m-%d") if rent_end_date else None
                        
                        total_paid = len(paid_months)*float(monthly_rent)
                        booking = models.Booking.objects.create(
                            customer = customer,
                            shop = s,
                            monthly_rent = monthly_rent if monthly_rent else 0,
                            advance_payment = advance if advance else 0,
                            advance_payment_date = advance_payment_date,
                            total_paid = total_paid,
                            rent_start_date = start_date,
                            end_date = rent_end_date,
                            is_ended = False if rent_end_date is None else True,
                        )

                        for month,date in paid_months.items():
                            rent_date = datetime.strptime(date, "%d-%m-%Y") if date else None
                            rent_date = rent_date.strftime("%Y-%m-%d") if rent_date else None

                            if(rent_date):
                                models.MonthlyPayment.objects.create(
                                    booking = booking,
                                    date = rent_date,
                                    month = month,
                                    amount = monthly_rent,
                                )

            context = {
                    "status": 200,
                    "message": "Customers Successfully Updated"
                }

            return JsonResponse(context,status=200)

        except Exception as e:
            traceback.print_exc()
            ic(e)
            context = {
                    "status":501,
                    "message": "Internal Server Error",
                    "error": str(e)
                }
            return JsonResponse(context,status=501)

class MakePayment(LoginRequiredMixin, View):
    def __init__(self) -> None:
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

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
            
class PaymentDetails(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

    def get(self, request, id):
        details = models.MonthlyPayment.objects.filter(booking_id = id).values()
        # json_details = serialize("json",details)
        return JsonResponse({'details': list(details)})

class Customer(LoginRequiredMixin, View):
    def __init__(self) -> None:
        self.login_url = reverse('admin:login')  # Custom login URL
        self.redirect_field_name = 'next'

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

        ic(name,email,number,address,nid)
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
        body = json.loads(request.body.decode('utf-8'))

        id = body.get('id', None)
        name = body.get('name', None)
        email = body.get('email', None)
        number = body.get('number', None)
        nid = body.get('nid', None)
        address = body.get('address', None)

        try:
            if id and name and number and address:
                customer = models.Customer.objects.filter(id=id.replace("#","")).first()

                if not customer:
                    self.context['status'] = 400
                    self.context['message'] = 'Customer not found'
                    return JsonResponse(self.context, status=400)

                customer.name = name
                customer.email = email
                customer.number = number
                customer.nid = nid
                customer.address = address

                customer.save()
                # self.context['customers'] = models.Customer.objects.all()
                self.context['status'] = 200
                self.context['message'] = 'Customer successfully updated'
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

    def delete(self,request):
        body = json.loads(request.body.decode('utf-8'))

        id = body.get('id',None)

        if id is None:
            context = {
                "status": 400,
                "message": "Missing required fields"
            }
            return JsonResponse(context,status=400)
        
        customer = models.Customer.objects.filter(id=id).first()

        if not customer:
            context = {
                "status": 400,
                "message": "Unknown customer information"
            }
            return JsonResponse(context,status=400)
        
        try:
            customer.delete()
            context = {
                "status": 200,
                "message": "Customer deleted successfully"
            }
            return JsonResponse(context,status=200)
        
        except Exception as e:
            traceback.print_exc()
            context = {
                "status": 501,
                "message": "Internal Server Error",
                "error": str(e)
            }
            return JsonResponse(context,status=200)
        