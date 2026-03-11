from django.contrib import admin
from .models import Card
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.exceptions import FieldError
# Register your models here

class CardResource(resources.ModelResource):

    class Meta:
        model = Card

    
    def before_import_row(self, row, **kwargs):
        print(row)
        raise FieldError("bu xato")
        # return super().before_import_row(row, **kwargs)
    

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

