from django.db import models
from student.models import Student
from academics.models import SchoolClass, Subject, Section

class Grade(models.Model):
    name = models.CharField(max_length=5) # A+, A, B, etc.
    min_mark = models.IntegerField()
    max_mark = models.IntegerField()
    point = models.DecimalField(max_digits=3, decimal_places=2) # 5.00, 4.00
    
    # START: GRADE_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: GRADE_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.name} ({self.min_mark}-{self.max_mark})"

class Exam(models.Model):
    name = models.CharField(max_length=100) # Final Exam, Half Yearly
    year = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)
    exam_type = models.CharField(max_length=20, choices=[('Class Test', 'Class Test'), ('Half-Yearly', 'Half-Yearly'), ('Annual', 'Annual')], default='Class Test')
    created_by_teacher = models.ForeignKey('teacher.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_exams')
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.year}"

class ExamSchedule(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    room_number = models.CharField(max_length=20, blank=True, null=True) # make room_number optional since Class Test might not have room number or might use classroom.
    total_marks = models.IntegerField(default=100)
    instructions = models.TextField(blank=True, null=True)
    
    # START: EXAMSCHEDULE_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: EXAMSCHEDULE_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.exam.name} - {self.subject.name} ({self.school_class.name})"

class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    # START: STUDENTRESULT_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: STUDENTRESULT_REMINDER_FIELDS
    
    class Meta:
        unique_together = ('student', 'exam', 'subject')
    
    def __str__(self):
        return f"{self.student.student_id} - {self.subject.name} - {self.marks_obtained}"
