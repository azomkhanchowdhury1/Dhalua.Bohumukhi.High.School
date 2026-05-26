from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile', null=True, blank=True)
    profile_image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(null=True, blank=True)

    teacher_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} ({self.teacher_id})"
        return f"Teacher {self.teacher_id or self.id}"

class SalaryPayment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salary_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=10)
    payment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])

    def __str__(self):
        return f"{self.teacher} - {self.month} {self.year}"

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
