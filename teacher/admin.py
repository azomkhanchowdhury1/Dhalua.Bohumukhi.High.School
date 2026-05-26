from django.contrib import admin
from .models import Teacher
from .forms import TeacherAdminForm

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('teacher_id', 'get_first_name', 'get_last_name', 'department', 'subject')
    search_fields = ('teacher_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'
