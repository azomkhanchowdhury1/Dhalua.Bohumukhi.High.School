from django.db import models

class SchoolClass(models.Model):
    name = models.CharField(max_length=50) # e.g. Class 6, Class 10
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School Classes"

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
    GROUP_CHOICES = (
        ('Science', 'Science'),
        ('Commerce', 'Commerce'),
        ('Humanities', 'Humanities'),
        ('General', 'General'),
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='syllabus/')
    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='General', help_text="The curriculum group this syllabus belongs to.")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # START: SYLLABUS_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: SYLLABUS_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.subject.name} Syllabus ({self.group})"

    class Meta:
        verbose_name_plural = "Syllabuses"

# START: ONLINE_CLASS_MODEL
class OnlineClass(models.Model):
    STATUS_CHOICES = [
        ('Live', 'Live'),
        ('Scheduled', 'Scheduled'),
        ('Recorded', 'Recorded')
    ]
    title = models.CharField(max_length=200) # e.g. Mathematics - Chapter 5
    topic = models.CharField(max_length=255, blank=True, null=True) # e.g. Quadratic Equations...
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE, related_name='online_classes')
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True, blank=True, related_name='online_classes')
    start_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    meeting_link = models.URLField(blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True)
    duration_minutes = models.IntegerField(default=45)
    students_count = models.IntegerField(default=0) # For mockup display

    def __str__(self):
        return f"{self.title} - {self.status}"
# END: ONLINE_CLASS_MODEL

# START: CLASS_ROUTINE_MODEL
class ClassRoutine(models.Model):
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='routines')
    title = models.CharField(max_length=200, default='Class Routine')
    file = models.FileField(upload_to='routines/', help_text="Upload the routine file (PDF, image, etc.)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school_class.name} - {self.title}"

    class Meta:
        verbose_name_plural = "Class Routines"
        ordering = ['school_class__name']
# END: CLASS_ROUTINE_MODEL
