from django.contrib import admin
from .models import Gallery

# START: GALLERY_ADMIN
@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)
# END: GALLERY_ADMIN
