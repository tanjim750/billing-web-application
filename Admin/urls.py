from django.urls import path
from . import views

urlpatterns = [
    path('', views.SalesListView.as_view(), name="booking-list"),
    path('new-booking', views.NewBooking.as_view(), name="new-booking"),
    path('new-customer',views.NewBooking.as_view(),name='new-customer'),
    path('customer',views.Customer.as_view(),name='customer-list'),
    path('make-payment',views.MakePayment.as_view(),name='make-payment'),
    path('payment-details/<id>',views.PaymentDetails.as_view(),name='payment-details')
]
