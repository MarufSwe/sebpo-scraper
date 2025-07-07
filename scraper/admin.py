from django.contrib import admin
from .models import ScrapedItem

# Register your models here.
@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'finding_date', 'nprm_date', 'final_rule_date', 'rescinded_date', 'last_updated']
    