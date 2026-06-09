from django.contrib import admin
from django.utils.html import format_html
from .models import Gallery

# START: GALLERY_ADMIN
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'media_preview', 'is_remembered', 'created_at')
    list_filter = ('category', 'is_remembered')
    search_fields = ('title',)
    
    fieldsets = (
        ('Media Information', {
            'fields': (
                ('title', 'category'),
                'file'
            )
        }),
        ('Settings', {
            'fields': (
                'is_remembered',
                'reminder_note'
            )
        }),
    )

    def media_preview(self, obj):
        if obj.file:
            if obj.category == 'image':
                return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius:8px;" />', obj.file.url)
            elif obj.category == 'video':
                return format_html('<video src="{}" style="max-height: 50px; max-width: 50px; border-radius:8px;" muted></video>', obj.file.url)
        return "No Media"
    media_preview.short_description = 'Preview'
# END: GALLERY_ADMIN
