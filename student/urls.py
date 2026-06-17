from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.dashboard, name='student_dashboard'),
    path('attendance/detail/', views.attendance_detail, name='attendance_detail'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('activity-log/', views.activity_log, name='activity_log'),
    
    # Academic Section
    path('academic/timetable/', views.academic_timetable, name='academic_timetable'),
    path('academic/syllabus/', views.academic_syllabus, name='academic_syllabus'),
    path('academic/teachers/', views.academic_teachers, name='academic_teachers'),
    path('academic/teachers/message/', views.message_teacher, name='message_teacher'),
    path('academic/calendar/', views.academic_calendar, name='academic_calendar'),
    
    # Exams & Results
    path('exam/routine/', views.exam_routine, name='exam_routine'),
    path('exam/results/', views.exam_results, name='exam_results'),
    path('exam/analytics/', views.exam_analytics, name='exam_analytics'),
    path('exam/admit-card/', views.exam_admit_card, name='exam_admit_card'),

    # Learning Tools
    path('learning/homework/', views.learning_homework, name='learning_homework'),
    path('learning/study-material/', views.learning_study_material, name='learning_study_material'),
    path('learning/library/', views.learning_library, name='learning_library'),
    path('learning/online-class/', views.learning_online_class, name='learning_online_class'),

    # Fees & Dues
    path('fees/pay/', views.fees_pay, name='fees_pay'),
    path('fees/history/', views.fees_history, name='fees_history'),
    path('fees/structure/', views.fees_structure, name='fees_structure'),
]
