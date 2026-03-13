from django.contrib import admin
from .models import Card
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.exceptions import FieldError, ImportError
import re
# Register your models here

class CardResource(resources.ModelResource):

    class Meta:
        model = Card

    def normalize_date(self, x):
        x = str(x).strip()

        if re.match(r"^\d{4}-\d{2}-\d{2}$", x):
            return x

        elif re.match(r"^\d{4}-\d{2}$", x):
            return f"{x}-01"

        elif re.match(r"^\d{2}\.\d{4}$", x):
            m, y = x.split(".")
            return f"{y}-{m}-01"

        elif re.match(r"^\d{2}/\d{2}$", x):
            m, y = x.split("/")
            return f"20{y}-{m}-01"

        return x

    def before_import_row(self, row, **kwargs):
        if "card_number" not in row:
            raise ImportError("card_number field bo'lishi majburiy!")
        elif "phone" not in row:
            raise ImportError("phone field bo'lishi majburiy!")
        card_number = str(row.get("card_number"))
        card_number = card_number.replace("-", "").replace(" ", "")
        if len(card_number) != 16:
            raise ImportError(f"Karta raqam 16 xonadan iborat emas! shu malumot: {card_number}")
        phone_number = str(row.get("phone"))
        phone_number = phone_number.replace("-", "").replace(" ", "")
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number
        if not phone_number.startswith("+998"):
            phone_number = "+998" + phone_number[1:]
        if len(phone_number) != 13:
            raise ImportError(f"Telefon raqam notog'ri formatda. togri format; +998901234567! sizdagi malumot: {phone_number}")
        expired_date = str(row.get("expired"))
        expired_date = self.normalize_date(expired_date)
        balance = str(row.get("balance"))
        balance = balance.replace(" ", "").replace(",", "")
        row['balance'] = balance
        row['phone'] = phone_number
        row['card_number'] = card_number
        row['expired'] = expired_date
        return super().before_import_row(row, **kwargs)
    

@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    resource_classes = [CardResource]
    list_display = ("format_card", "format_phone", "balance", "status", "expired")
    list_filter = ("status", "expired")

    def format_card(self, obj):
        # 8600 1234 5678 9012
        return f"{obj.card_number[:4]} {obj.card_number[4:8]} {obj.card_number[8:12]} {obj.card_number[12:16]}"

    def format_phone(self, obj):
        # +998 90 123 45 67
        return f"{obj.phone[:4]} {obj.phone[4:6]} {obj.phone[6:9]} {obj.phone[9:11]} {obj.phone[11:13]}"

