# START: student/models.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    password_plain = models.CharField(max_length=128, blank=True, null=True, verbose_name="Current Password")
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

    @property
    def full_info(self):
        name = ""
        if self.user:
            name = self.user.get_full_name().strip()
        if not name:
            name = self.student_id or ""
        roll = self.roll_number or "N/A"
        klass = self.current_class or "N/A"
        return f"{name} (Roll: {roll}, Class: {klass})"

class ClassAttendance(models.Model):
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.SET_NULL, null=True, related_name='classes_taken')
    school_class = models.ForeignKey('academics.SchoolClass', on_delete=models.CASCADE, related_name='attendances')
    section = models.ForeignKey('academics.Section', on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    is_held = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.school_class} - {self.subject} on {self.date}"

class Attendance(models.Model):
    class_attendance = models.ForeignKey(ClassAttendance, on_delete=models.CASCADE, related_name='student_attendances', null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late'), ('Leave', 'Leave')])
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'class_attendance')
        verbose_name_plural = "Attendance"

class PromotionHistory(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    from_class = models.CharField(max_length=20)
    to_class = models.CharField(max_length=20)
    from_year = models.CharField(max_length=10)
    to_year = models.CharField(max_length=10)
    promotion_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} promoted to {self.to_class}"

    class Meta:
        verbose_name_plural = "Promotion Histories"

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
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_homeworks')
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.title}"

    class Meta:
        verbose_name_plural = "Student Homework"

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
# END: student/models.py
