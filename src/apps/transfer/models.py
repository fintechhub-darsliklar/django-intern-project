from django.db import models
from django.core.validators import MaxValueValidator
import uuid
from apps.card.models import Card

class TransferState(models.TextChoices):
    CREATED = 'created', 'Created'
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'

class Transfer(models.Model):
    ext_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sender_card = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name='sent_transfers'
    )
    receiver_card = models.ForeignKey(
        Card, on_delete=models.PROTECT, related_name='received_transfers'
    )
    
    sender_card_expiry = models.CharField(max_length=5, help_text="Format: MM/YY")
    sender_phone = models.CharField(max_length=20, blank=True, null=True)
    receiver_phone = models.CharField(max_length=20, blank=True, null=True)
    sending_amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(
        max_length=3, 
        choices=[('643', 'RUB'), ('840', 'USD')],
        default='840'
    )
    receiving_amount = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    
    # Holat va Xavfsizlik
    state = models.CharField(
        max_length=10, 
        choices=TransferState.choices, 
        default=TransferState.CREATED
    )
    try_count = models.PositiveSmallIntegerField(
        default=0, 
        validators=[MaxValueValidator(3)]
    )
    otp = models.CharField(max_length=6, blank=True, null=True)
    
    # Vaqt ko'rsatkichlari
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Receiving amountni avtomatik hisoblash (Masalan: statik kurs 1 USD = 12,800 so'm)
        # Bu yerda biznes mantiqni yozishingiz mumkin
        if not self.receiving_amount:
            static_rate = 12800 # Misol uchun
            self.receiving_amount = self.sending_amount * static_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transfer {self.ext_id} - {self.state}"
    



class Error(models.Model):
    code = models.IntegerField(unique=True, help_text="Xatolik kodi")
    en = models.CharField(max_length=255, verbose_name="English")
    ru = models.CharField(max_length=255, verbose_name="Russian")
    uz = models.CharField(max_length=255, verbose_name="Uzbek")

    def __str__(self):
        return f"{self.code} - {self.en}"

    class Meta:
        verbose_name = "Error Message"
        verbose_name_plural = "Error Messages"