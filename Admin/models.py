from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=500)
    number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100 , blank=True, null=True)
    address = models.TextField()
    nid = models.CharField(max_length=100, blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name.strip()
    

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop = models.CharField(max_length=10000)
    monthly_rent = models.FloatField(default=0)
    advance_payment = models.FloatField(default=0)
    advance_payment_date = models.DateTimeField(null=True, blank=True)
    total_paid = models.FloatField(default=0)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    rent_start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop.strip()

class MonthlyPayment(models.Model):
    choices = [
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=100, choices=choices)
    amount = models.FloatField()
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.booking.shop}: {self.month}"

class Logo(models.Model):
    normal = models.FileField(upload_to="logo")
    white = models.FileField(upload_to="logo")
    small = models.FileField(upload_to="logo")
    icon = models.FileField(upload_to="logo",null=True)

    