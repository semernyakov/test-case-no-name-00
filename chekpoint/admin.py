from django.contrib import admin
from .models import KeyBox


@admin.register(KeyBox)
class AdminKeyBox(admin.ModelAdmin):
    list_display = ['id', 'key_code', 'activation_status', 'issue_status',
                    'keys_amount', 'pub_date', 'end_date', 'owner']
    show_full_result_count = True
    search_fields = ['key_code', 'id']
