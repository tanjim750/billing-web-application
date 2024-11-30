from django.urls import path
from . import views

urlpatterns = [
    path('', views.SalesListView.as_view(), name="booking-list"),
    path('booking', views.Booking.as_view(), name="new-booking"),
    path('customer',views.Customer.as_view(),name='customer-list'),
    path('make-payment',views.MakePayment.as_view(),name='make-payment'),
    path('payment-details/<id>',views.PaymentDetails.as_view(),name='payment-details'),
    path('import-booking',views.ImportBooking.as_view(),name='import-booking'),
    path('logout/',views.Logout.as_view(),name='logout'),
]
