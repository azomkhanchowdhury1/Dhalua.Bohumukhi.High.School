from django.db import models
from django.contrib.auth.models import User

# Notice model for School Management System
# Public notice, Role-based notice, Multi-role notice

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_public = models.BooleanField(default=False, help_text="Public notices are visible to everyone without login.")
    
    # Target Roles
    target_student = models.BooleanField(default=False, verbose_name="Student")
    target_teacher = models.BooleanField(default=False, verbose_name="Teacher")
    target_staff = models.BooleanField(default=False, verbose_name="Staff")
    target_parent = models.BooleanField(default=False, verbose_name="Parent")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Signature and Downloads
    signature = models.ImageField(upload_to='notices/signatures/', null=True, blank=True, help_text="Upload headmaster's signature image.")
    attachment = models.FileField(upload_to='notices/attachments/', null=True, blank=True, help_text="Upload official PDF or Image notice.")

    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notice"
        verbose_name_plural = "Notices"
