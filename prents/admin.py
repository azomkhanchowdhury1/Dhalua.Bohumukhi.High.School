from django.contrib import admin
from .models import Parent
from .forms import ParentAdminForm

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    form = ParentAdminForm
    list_display = ('parent_id', 'get_first_name', 'get_last_name', 'linked_student', 'phone_number')
    search_fields = ('parent_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number', 'linked_student__student_id')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'
