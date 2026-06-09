from django.contrib import admin
from django.utils.html import format_html
from .models import Event

# START: EVENT_ADMIN
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'image_preview', 'is_remembered')
    list_filter = ('date', 'is_remembered')
    search_fields = ('title', 'location', 'description')
    
    fieldsets = (
        ('Event Information', {
            'fields': (
                'title',
                ('date', 'time'),
                'location',
                'description'
            )
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': (
                'is_remembered',
                'reminder_note'
            )
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius:8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Event Image'
# END: EVENT_ADMIN
