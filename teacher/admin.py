# START: teacher/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Teacher, SalaryPayment, TeacherAssignment
from .forms import TeacherAdminForm

# START: TEACHER_ADMIN
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('teacher_id', 'get_first_name', 'get_last_name', 'department', 'subject', 'password_plain', 'image_preview')
    readonly_fields = ('password_plain',)
    search_fields = ('teacher_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')
    list_filter = ('gender', 'department', 'blood_group')

    fieldsets = (
        ('Account Credentials', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('password', 'confirm_password'),
                'password_plain',
            )
        }),
        ('Personal Information', {
            'fields': (
                ('phone_number', 'date_of_birth'),
                ('gender', 'blood_group'),
                ('profile_image', 'address'),
            )
        }),
        ('Professional Information', {
            'fields': (
                ('teacher_id', 'joining_date'),
                ('department', 'subject'),
                ('qualification', 'experience'),
                'salary'
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
# END: TEACHER_ADMIN

# START: TEACHER_SALARY_PAYMENT_ADMIN
@admin.register(SalaryPayment)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'amount', 'month', 'year', 'status', 'payment_date')
    list_filter = ('status', 'month', 'year')
    search_fields = ('teacher__teacher_id', 'teacher__user__first_name')
    fieldsets = (
        ('Payment Details', {
            'fields': (
                'teacher',
                'amount', 'status',
                'month', 'year'
            )
        }),
    )
# END: TEACHER_SALARY_PAYMENT_ADMIN

# START: TEACHER_ASSIGNMENT_ADMIN
@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'due_date', 'status', 'assigned_at')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'teacher__teacher_id', 'teacher__user__first_name')
    fieldsets = (
        ('Assignment Details', {
            'fields': (
                'teacher', 'status',
                'title', 'due_date',
                'description'
            )
        }),
    )
# END: TEACHER_ASSIGNMENT_ADMIN

# END: teacher/admin.py
