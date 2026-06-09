from django.contrib import admin
from .models import SchoolClass, Section, Subject, Timetable, Syllabus, OnlineClass

# START: SCHOOLCLASS_ADMIN
@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    fieldsets = (
        ('Class Details', {
            'fields': (('name', 'code'),)
        }),
    )
# END: SCHOOLCLASS_ADMIN

# START: SECTION_ADMIN
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'school_class', 'room_number')
    list_filter = ('school_class',)
    search_fields = ('name', 'room_number', 'school_class__name')
    fieldsets = (
        ('Section Details', {
            'fields': (
                ('school_class', 'name'),
                'room_number'
            )
        }),
    )
# END: SECTION_ADMIN

# START: SUBJECT_ADMIN
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school_class', 'is_remembered')
    list_filter = ('school_class', 'is_remembered')
    search_fields = ('name', 'code', 'school_class__name')
    fieldsets = (
        ('Subject Details', {
            'fields': (
                ('name', 'code'),
                'school_class'
            )
        }),
        ('Settings', {
            'fields': (
                ('is_remembered', 'reminder_note'),
            )
        }),
    )
# END: SUBJECT_ADMIN

# START: TIMETABLE_ADMIN
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('section', 'subject', 'day', 'start_time', 'end_time', 'is_remembered')
    list_filter = ('day', 'section__school_class', 'is_remembered')
    search_fields = ('section__name', 'subject__name')
    fieldsets = (
        ('Timetable Entry', {
            'fields': (
                ('section', 'subject'),
                'day',
                ('start_time', 'end_time')
            )
        }),
        ('Settings', {
            'fields': (
                ('is_remembered', 'reminder_note'),
            )
        }),
    )
# END: TIMETABLE_ADMIN

# START: SYLLABUS_ADMIN
@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'uploaded_at', 'is_remembered')
    list_filter = ('subject', 'is_remembered')
    search_fields = ('title', 'subject__name')
    fieldsets = (
        ('Syllabus File', {
            'fields': (
                ('subject', 'title'),
                'file'
            )
        }),
        ('Settings', {
            'fields': (
                ('is_remembered', 'reminder_note'),
            )
        }),
    )
# END: SYLLABUS_ADMIN

# START: ONLINECLASS_ADMIN
@admin.register(OnlineClass)
class OnlineClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'school_class', 'status', 'start_time', 'duration_minutes')
    list_filter = ('status', 'school_class')
    search_fields = ('title', 'topic', 'teacher__user__first_name')
    fieldsets = (
        ('Class Details', {
            'fields': (
                ('title', 'topic'),
                ('teacher', 'school_class'),
            )
        }),
        ('Session Info', {
            'fields': (
                ('status', 'start_time', 'duration_minutes'),
                'meeting_link',
                'recording_url',
                'students_count',
            )
        }),
    )
# END: ONLINECLASS_ADMIN
