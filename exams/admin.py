from django.contrib import admin
from .models import Grade, Exam, ExamSchedule, StudentResult

# START: GRADE_ADMIN
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_mark', 'max_mark', 'point', 'is_remembered')
    search_fields = ('name',)
    fieldsets = (
        ('Grade Details', {
            'fields': (
                ('name', 'point'),
                ('min_mark', 'max_mark')
            )
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: GRADE_ADMIN

# START: EXAM_ADMIN
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'is_active')
    list_filter = ('year', 'is_active')
    search_fields = ('name', 'year')
    fieldsets = (
        ('Exam Details', {
            'fields': (
                ('name', 'year'),
                'is_active'
            )
        }),
    )
# END: EXAM_ADMIN

# START: EXAMSCHEDULE_ADMIN
@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ('exam', 'subject', 'school_class', 'date', 'start_time', 'room_number', 'is_remembered')
    list_filter = ('exam', 'school_class', 'date', 'is_remembered')
    search_fields = ('exam__name', 'subject__name', 'room_number')
    fieldsets = (
        ('Schedule Entry', {
            'fields': (
                ('exam', 'school_class'),
                'subject',
                ('date', 'start_time'),
                'room_number'
            )
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: EXAMSCHEDULE_ADMIN

# START: STUDENTRESULT_ADMIN
@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'subject', 'marks_obtained', 'grade', 'is_remembered')
    list_filter = ('exam', 'subject', 'grade', 'is_remembered')
    search_fields = ('student__student_id', 'student__user__first_name', 'subject__name')
    fieldsets = (
        ('Result Information', {
            'fields': (
                ('student', 'exam'),
                'subject',
                ('marks_obtained', 'grade'),
                'remarks'
            )
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: STUDENTRESULT_ADMIN
