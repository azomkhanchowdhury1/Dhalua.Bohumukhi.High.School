from django.contrib import admin
from django.utils.html import format_html
from .models import Staff
from .forms import StaffAdminForm

# START: STAFF_ADMIN
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    form = StaffAdminForm
    list_display = ('staff_id', 'get_first_name', 'get_last_name', 'designation', 'department', 'image_preview')
    search_fields = ('staff_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')
    list_filter = ('gender', 'department', 'work_shift')

    fieldsets = (
        ('Account Credentials', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('password', 'confirm_password'),
            )
        }),
        ('Personal Information', {
            'fields': (
                ('phone_number', 'date_of_birth'),
                ('gender', 'profile_image'),
                'address',
            )
        }),
        ('Professional Information', {
            'fields': (
                ('staff_id', 'joining_date'),
                ('designation', 'department'),
                ('work_shift', 'salary')
            )
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;" />', obj.profile_image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'

from .models import (
    LeaveRequest, ProblemReport, InventoryRequest, DutySchedule,
    AttendanceLog, DirectMessage, TaskAssignment, SalaryPayment,
    Holiday, EmergencyRequest, Document, EventDuty, PerformanceRecord, VisitorLog
)

admin.site.register(LeaveRequest)
admin.site.register(ProblemReport)
admin.site.register(InventoryRequest)
admin.site.register(DutySchedule)
admin.site.register(AttendanceLog)
admin.site.register(DirectMessage)
admin.site.register(TaskAssignment)
admin.site.register(SalaryPayment)
admin.site.register(Holiday)
admin.site.register(EmergencyRequest)
admin.site.register(Document)
admin.site.register(EventDuty)
admin.site.register(PerformanceRecord)
admin.site.register(VisitorLog)

# END: STAFF_ADMIN
