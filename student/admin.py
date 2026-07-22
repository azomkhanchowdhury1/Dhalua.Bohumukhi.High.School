# START: student/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Attendance, PromotionHistory, StudentActivityLog, StudentHomework, StudyMaterial, LibraryBook
from .forms import StudentAdminForm

# START: STUDENT_ADMIN
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('student_id', 'get_first_name', 'get_last_name', 'current_class', 'roll_number', 'password_plain', 'image_preview')
    readonly_fields = ('password_plain',)
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__username', 'phone_number')
    list_filter = ('gender', 'blood_group', 'current_class', 'academic_year')

    fieldsets = (
        ('Account Credentials', {
            'fields': (
                ('username', 'email'),
                ('first_name', 'last_name'),
                ('password', 'confirm_password'),
                'password_plain',
            )
        }),
        ('Personal Information', {
            'fields': (
                ('phone_number', 'date_of_birth'),
                ('gender', 'blood_group'),
                ('profile_image', 'address'),
            )
        }),
        ('Academic Information', {
            'fields': (
                ('student_id', 'roll_number'),
                ('admission_date', 'current_class'),
                ('section', 'academic_year'),
            )
        }),
    )

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else "N/A"
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else "N/A"
    get_last_name.short_description = 'Last Name'

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;" />', obj.profile_image.url)
        return "No Image"
    image_preview.short_description = 'Profile Image'
# END: STUDENT_ADMIN

# START: ATTENDANCE_ADMIN
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__student_id', 'student__user__first_name')
    fieldsets = (
        ('Attendance Details', {
            'fields': ('student', 'date', 'status', 'remarks')
        }),
    )
# END: ATTENDANCE_ADMIN

# START: PROMOTION_HISTORY_ADMIN
@admin.register(PromotionHistory)
class PromotionHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_class', 'to_class', 'from_year', 'to_year', 'promotion_date')
    search_fields = ('student__student_id', 'student__user__first_name')
    fieldsets = (
        ('Promotion Details', {
            'fields': (
                'student',
                'from_class', 'to_class',
                'from_year', 'to_year'
            )
        }),
    )
# END: PROMOTION_HISTORY_ADMIN

# START: STUDENT_ACTIVITY_LOG_ADMIN
@admin.register(StudentActivityLog)
class StudentActivityLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'action', 'timestamp')
    search_fields = ('student__student_id', 'action')
    fieldsets = (
        ('Activity Log', {
            'fields': ('student', 'action', 'details')
        }),
    )
# END: STUDENT_ACTIVITY_LOG_ADMIN

# START: STUDENT_HOMEWORK_ADMIN
@admin.register(StudentHomework)
class StudentHomeworkAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'subject', 'submitted_at')
    search_fields = ('student__student_id', 'title', 'subject')
    fieldsets = (
        ('Homework Details', {
            'fields': (
                'student', 'subject',
                'title',
                'description',
                'file'
            )
        }),
    )
# END: STUDENT_HOMEWORK_ADMIN

# START: STUDY_MATERIAL_ADMIN
@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'school_class', 'uploaded_at')
    search_fields = ('title', 'school_class__name')
    fieldsets = (
        ('Study Material', {
            'fields': (
                'school_class', 'title',
                'description',
                'file'
            )
        }),
    )
# END: STUDY_MATERIAL_ADMIN

# START: LIBRARY_BOOK_ADMIN
@admin.register(LibraryBook)
class LibraryBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'status', 'copies_available')
    search_fields = ('title', 'author', 'isbn', 'category')
    list_filter = ('status', 'category')
    fieldsets = (
        ('Book Information', {
            'fields': (
                'title', 'author',
                'isbn', 'category',
                'copies_available', 'status'
            )
        }),
    )
# END: LIBRARY_BOOK_ADMIN

# END: student/admin.py
