from django.urls import path
from . import views

app_name = 'prents'

urlpatterns = [
    path('dashboard/', views.dashboard, name='parent_dashboard'),
    
    # Academic Progress
    path('report-cards/', views.report_cards, name='report_cards'),
    path('performance-analytics/', views.performance_analytics, name='performance_analytics'),
    path('subject-syllabus/', views.subject_syllabus, name='subject_syllabus'),
    
    # Attendance
    path('monthly-summary/', views.monthly_summary, name='monthly_summary'),
    path('detailed-absence-log/', views.detailed_absence_log, name='detailed_absence_log'),
    path('leave-notification/', views.leave_notification, name='leave_notification'),
    
    # Finance & Fees
    path('pay-online/', views.pay_online, name='pay_online'),
    path('payment-receipts/', views.payment_receipts, name='payment_receipts'),
    path('fee-structure/', views.fee_structure, name='fee_structure'),
    
    # Exams & Routine
    path('exam-schedule/', views.exam_schedule, name='exam_schedule'),
    path('class-timetable/', views.class_timetable, name='class_timetable'),
    path('download-admit-card/', views.download_admit_card, name='download_admit_card'),
    
    # School Info
    path('academic-calendar/', views.academic_calendar, name='academic_calendar'),
    path('transport-status/', views.transport_status, name='transport_status'),
    path('canteen-menu/', views.canteen_menu, name='canteen_menu'),
]
