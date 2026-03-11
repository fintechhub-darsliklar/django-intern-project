from django.db import models

# Create your models here.

class Card(models.Model):
    card_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=(
        ("active", "Active"),
        ("in_active", "In Active"),
        ("expired", "Expired"),
    ))
    expired  = models.DateField()

    def __str__(self):
        return f"{self.card_number}, {self.phone}"