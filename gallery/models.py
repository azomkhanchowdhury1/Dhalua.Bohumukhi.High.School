from django.db import models

# START: GALLERY_MODEL
class Gallery(models.Model):
    CATEGORY_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='gallery/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='image')
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Galleries"
# END: GALLERY_MODEL
