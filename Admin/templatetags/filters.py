from django import template
from Admin.models import Booking

from datetime import datetime
from dateutil.relativedelta import relativedelta

from icecream import ic

register = template.Library()

@register.filter(name="total_due")
def get_booking_payment_due(booking: Booking, is_status = False):
    last_pay = booking.last_payment_date
    total_paid = booking.total_paid
    rent_start = booking.rent_start_date
    monthly_rent = booking.monthly_rent
    end_date = booking.end_date

    crnt_date = end_date.date() if end_date else datetime.now().date()
    date_diff = relativedelta(crnt_date,rent_start.date())

    total_months = date_diff.years * 12 + date_diff.months
    total_paying_rent = total_months * monthly_rent
    
    total_due = total_paying_rent - total_paid

    if not is_status:
        if total_due > 0:
            return total_due
        else:
            return 0
        
    else:
        if total_due == 0:
            return "PAID"
        elif total_due < 0:
            return "ADVANCED"
        else:
            return "DUE"


@register.filter(name="advance_rent")
def get_advance_rent(booking: Booking):
    last_pay = booking.last_payment_date
    total_paid = booking.total_paid
    rent_start = booking.rent_start_date
    monthly_rent = booking.monthly_rent
    end_date = booking.end_date

    crnt_date = end_date.date() if end_date else datetime.now().date()
    date_diff = relativedelta(crnt_date,rent_start.date())

    total_months = date_diff.years * 12 + date_diff.months
    total_paying_rent = total_months * monthly_rent
    
    advance_rent = total_paid - total_paying_rent

    if advance_rent > 0:
        return advance_rent
    else:
        return 0

    