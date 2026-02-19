from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('pharmacy', 'Pharmacy'),
        ('user', 'User'),
        ('delivery', 'Delivery Boy'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    view_password = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

class Pharmacy(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    location = models.CharField(max_length=255) # Detailed address
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, default='pending') # approve, reject, block
    image = models.ImageField(upload_to='pharmacy_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class DeliveryBoy(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return self.name

class Medicine(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    details = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='medicine_images/', null=True, blank=True)
    CATEGORY_CHOICES = (
        ('tablet', 'Tablet'),
        ('syrup', 'Syrup'),
        ('ointment', 'Ointment'),
        ('equipment', 'Equipment'),
        ('kit', 'Kit'),
        ('other', 'Other'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    prescription_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='booked')
    payment_status = models.CharField(max_length=20, default='pending')
    prescription = models.ImageField(upload_to='prescriptions/', null=True, blank=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_status = models.CharField(max_length=20, default='pending')
    user_confirmed = models.BooleanField(default=False)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
