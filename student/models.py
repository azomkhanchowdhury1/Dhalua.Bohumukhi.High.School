from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    profile_image = models.ImageField(upload_to='students/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    current_class = models.CharField(max_length=20, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    academic_year = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} ({self.student_id})"
        return f"Student {self.student_id or self.id}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late'), ('Leave', 'Leave')])
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'date')

class PromotionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_class = models.CharField(max_length=20)
    to_class = models.CharField(max_length=20)
    from_year = models.CharField(max_length=10)
    to_year = models.CharField(max_length=10)
    promotion_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} promoted to {self.to_class}"

class StudentActivityLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.action} at {self.timestamp}"

# START: LEARNING_TOOLS_MODELS
class StudentHomework(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='homework/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.title}"

class StudyMaterial(models.Model):
    school_class = models.ForeignKey('academics.SchoolClass', on_delete=models.CASCADE, related_name='study_materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.school_class.name})"

class LibraryBook(models.Model):
    STATUS_CHOICES = [('Available', 'Available'), ('Issued', 'Issued')]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    copies_available = models.IntegerField(default=1)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.title} by {self.author}"
# END: LEARNING_TOOLS_MODELS
