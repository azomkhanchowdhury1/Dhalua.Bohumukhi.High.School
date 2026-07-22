# START: prents/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Parent
from .forms import ParentAdminForm

# START: PARENT_ADMIN
@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    form = ParentAdminForm
    list_display = ('parent_id', 'get_first_name', 'get_last_name', 'relationship_type', 'occupation', 'password_plain', 'image_preview')
    readonly_fields = ('password_plain',)
    search_fields = ('parent_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')
    list_filter = ('gender', 'relationship_type')

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
                ('gender', 'profile_image'),
                'address',
            )
        }),
        ('Parent Details', {
            'fields': (
                ('parent_id', 'occupation'),
                ('relationship_type', 'linked_student'),
                'emergency_contact_number'
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
# END: PARENT_ADMIN

# END: prents/admin.py
