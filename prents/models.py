# START: prents/models.py
from django.db import models
from django.contrib.auth.models import User
from student.models import Student

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile', null=True, blank=True)
    password_plain = models.CharField(max_length=128, blank=True, null=True, verbose_name="Current Password")
    profile_image = models.ImageField(upload_to='parents/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    parent_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    relationship_type = models.CharField(max_length=50, choices=[('Father', 'Father'), ('Mother', 'Mother'), ('Guardian', 'Guardian')], null=True, blank=True)
    linked_student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='parents')
    emergency_contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} ({self.parent_id})"
        return f"Parent {self.parent_id or self.id}"

# END: prents/models.py
