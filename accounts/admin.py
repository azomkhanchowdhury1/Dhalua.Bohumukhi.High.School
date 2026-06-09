import string
import random
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from django.utils.html import format_html
from .models import UserProfile, RegistrationRequest
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from prents.models import Parent as SchoolParent

from django.contrib.auth.admin import UserAdmin

# START: CUSTOM_USER_ADMIN
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
# END: CUSTOM_USER_ADMIN

# START: USER_PROFILE_ADMIN
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'is_verified', 'image_preview')
    list_filter = ('role', 'is_verified', 'is_remembered')
    search_fields = ('user__username', 'user__email', 'phone_number')
    
    fieldsets = (
        ('User Information', {
            'fields': (
                ('user', 'role'),
                'profile_image',
            )
        }),
        ('Personal Information', {
            'fields': (
                ('phone_number', 'date_of_birth'),
                ('gender', 'blood_group'),
                'address'
            )
        }),
        ('Verification & Settings', {
            'fields': (
                ('is_verified', 'otp_code'),
                ('is_remembered', 'reminder_note')
            )
        }),
    )

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;" />', obj.profile_image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'
# END: USER_PROFILE_ADMIN

# START: REGISTRATION_REQUEST_ADMIN
@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'role', 'is_approved', 'email_sent', 'created_at')
    list_filter = ('role', 'is_approved', 'email_sent', 'is_rejected')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    actions = ['approve_requests', 'reject_requests']
    
    fieldsets = (
        ('Request Details', {
            'fields': (
                ('first_name', 'last_name'),
                ('email', 'phone_number'),
                'role',
            )
        }),
        ('Additional Info', {
            'fields': ('additional_info',)
        }),
        ('Status', {
            'fields': (
                ('is_approved', 'is_rejected'),
                ('email_sent', 'is_remembered'),
                'reminder_note'
            )
        }),
    )

    def process_approval(self, req):
        """Helper method to handle the logic of creating user and sending email."""
        if not req.is_approved:
            return "not_approved", None
            
        if User.objects.filter(email=req.email).exists():
            return "exists", None
            
        # 1. Generate Username
        username = slugify(req.first_name + req.last_name)
        if User.objects.filter(username=username).exists():
            username = f"{username}{random.randint(10, 99)}"
        
        # 2. Generate Random Password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # 3. Create User
        user = User.objects.create_user(
            username=username,
            password=password,
            email=req.email,
            first_name=req.first_name,
            last_name=req.last_name
        )
        
        # 4. Create Role Profile
        if req.role == 'Student':
            Student.objects.create(user=user, phone_number=req.phone_number, student_id=f"STU{random.randint(1000, 9999)}")
        elif req.role == 'Teacher':
            Teacher.objects.create(user=user, phone_number=req.phone_number, teacher_id=f"TEA{random.randint(1000, 9999)}", salary=0)
        elif req.role == 'Staff':
            Staff.objects.create(user=user, phone_number=req.phone_number, staff_id=f"STA{random.randint(1000, 9999)}", salary=0)
        elif req.role == 'Parent':
            SchoolParent.objects.create(user=user, phone_number=req.phone_number, parent_id=f"PAR{random.randint(1000, 9999)}")

        # 5. Send Email
        subject = 'Your School Management System Account'
        message = f'Hello {req.first_name},\n\nYour registration request has been approved.\n\nUsername: {username}\nPassword: {password}\n\nYou can now login at: http://127.0.0.1:8000/accounts/login/\n\nRegards,\nSchool Admin'
        
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [req.email], fail_silently=False)
            req.email_sent = True
            req.save()
            return "success", None
        except Exception as e:
            error_msg = str(e)
            print(f"CRITICAL EMAIL ERROR: {error_msg}")
            return "email_failed", error_msg

    def save_model(self, request, obj, form, change):
        """Override save_model to trigger approval logic when saving from detail view."""
        is_newly_approved = False
        if change: # If updating an existing object
            old_obj = RegistrationRequest.objects.get(pk=obj.pk)
            if not old_obj.is_approved and obj.is_approved:
                is_newly_approved = True
        elif obj.is_approved: # If creating and already marked as approved
            is_newly_approved = True
            
        super().save_model(request, obj, form, change)
        
        if is_newly_approved:
            status, error_detail = self.process_approval(obj)
            if status == "success":
                self.message_user(request, f"User created and email sent to {obj.email}")
            elif status == "email_failed":
                self.message_user(request, f"User created but failed to send email to {obj.email}. Error: {error_detail}", level='error')
            elif status == "exists":
                self.message_user(request, f"User with email {obj.email} already exists. No new account created.", level='warning')

    def approve_requests(self, request, queryset):
        """Bulk action from list view."""
        count = 0
        for req in queryset.filter(is_approved=False):
            req.is_approved = True
            req.save()
            status, _ = self.process_approval(req)
            if status == "success":
                count += 1
        self.message_user(request, f"{count} requests approved and emails sent.")

    approve_requests.short_description = "Approve selected requests and Send Email"

    def reject_requests(self, request, queryset):
        queryset.update(is_rejected=True, is_approved=False)
    reject_requests.short_description = "Reject selected requests"
# END: REGISTRATION_REQUEST_ADMIN
