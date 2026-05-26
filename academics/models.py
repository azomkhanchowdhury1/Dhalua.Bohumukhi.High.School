from django.db import models

class SchoolClass(models.Model):
    name = models.CharField(max_length=50) # e.g. Class 6, Class 10
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Section(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10) # e.g. A, B, C
    room_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.school_class.name} - Section {self.name}"

class Subject(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    # START: SUBJECT_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: SUBJECT_REMINDER_FIELDS

    def __str__(self):
        return f"{self.name} ({self.school_class.name})"

class Timetable(models.Model):
    DAYS = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # START: TIMETABLE_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: TIMETABLE_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.section} - {self.subject} ({self.day})"

class Syllabus(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='syllabus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # START: SYLLABUS_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: SYLLABUS_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.subject.name} Syllabus"
