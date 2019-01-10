from django.contrib import admin
from .models import KeyCounter, KeyBox


@admin.register(KeyCounter)
class AdminKeyCounter(admin.ModelAdmin):
    list_display = ['keys_amount']


@admin.register(KeyBox)
class AdminKeyBox(admin.ModelAdmin):
    list_display = ['id', 'check_sum', 'key_code', 'activation_status',
                    'issue_status', 'key_amount', 'pub_date', 'end_date',
                    'owner']
    show_full_result_count = True
    search_fields = ['key_code', 'id']
    readonly_fields = ['check_sum', 'key_amount']

    def key_amount(self, obj):
        return obj.key_counter.keys_amount
