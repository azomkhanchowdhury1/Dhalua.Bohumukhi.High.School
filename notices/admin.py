from django.contrib import admin
from .models import Notice

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'target_student', 'target_teacher', 'target_staff', 'target_parent', 'created_at')
    list_filter = ('is_public', 'target_student', 'target_teacher', 'target_staff', 'target_parent', 'created_at')
    search_fields = ('title', 'content')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'is_public', 'signature', 'attachment')
        }),
        ('Target Roles', {
            'fields': ('target_student', 'target_teacher', 'target_staff', 'target_parent'),
            'description': "Select which roles should see this notice if it's not public."
        }),
        ('Meta Information', {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
