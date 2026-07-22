from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Staff', 'Staff'),
        ('Parent', 'Parent'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class RegistrationRequest(models.Model):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
        ('Staff', 'Staff'),
        ('Parent', 'Parent'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    additional_info = models.TextField(blank=True, null=True, help_text="Any additional info for verification")
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role}) - {'Approved' if self.is_approved else 'Pending'}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class SupportTicket(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    message = models.TextField()
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject} ({self.priority})"

# START: TESTIMONIAL_MODEL
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Parent, Guardian, Senior Teacher")
    quote = models.TextField(help_text="The testimonial quote text.")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Optional profile image.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.name} ({self.role})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Testimonials"
# END: TESTIMONIAL_MODEL
