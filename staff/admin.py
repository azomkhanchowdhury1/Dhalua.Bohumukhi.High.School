from django.contrib import admin
from .models import Staff
from .forms import StaffAdminForm

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ('staff_id', 'get_first_name', 'get_last_name', 'designation', 'department')
    search_fields = ('staff_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'
