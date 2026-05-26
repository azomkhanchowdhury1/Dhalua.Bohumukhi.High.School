from django.contrib import admin
from .models import Student
from .forms import StudentAdminForm

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('student_id', 'get_first_name', 'get_last_name', 'current_class', 'roll_number')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'
