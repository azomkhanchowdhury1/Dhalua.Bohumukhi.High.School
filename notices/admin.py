from django.contrib import admin
from django.utils.html import format_html
from .models import Notice

# START: NOTICE_ADMIN
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'target_summary', 'signature_preview', 'created_at')
    list_filter = ('is_public', 'target_student', 'target_teacher', 'target_staff', 'target_parent')
    search_fields = ('title', 'content')
    
    fieldsets = (
        ('Notice Details', {
            'fields': (
                'title',
                'content',
            )
        }),
        ('Target Audience', {
            'fields': (
                'is_public',
                ('target_student', 'target_teacher'),
                ('target_staff', 'target_parent'),
            )
        }),
        ('Media & Signatures', {
            'fields': (
                ('signature', 'attachment'),
            )
        }),
        ('Settings', {
            'fields': (
                ('is_remembered', 'reminder_note'),
                'created_by'
            )
        }),
    )

    def target_summary(self, obj):
        targets = []
        if obj.is_public: targets.append("Public")
        if obj.target_student: targets.append("Student")
        if obj.target_teacher: targets.append("Teacher")
        if obj.target_staff: targets.append("Staff")
        if obj.target_parent: targets.append("Parent")
        return ", ".join(targets) if targets else "None"
    target_summary.short_description = 'Target Audience'

    def signature_preview(self, obj):
        if obj.signature:
            return format_html('<img src="{}" style="max-height: 40px; border-radius:4px;" />', obj.signature.url)
        return "No Signature"
    signature_preview.short_description = 'Signature'
# END: NOTICE_ADMIN
