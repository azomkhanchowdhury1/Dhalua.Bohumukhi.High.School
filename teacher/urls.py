from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.dashboard, name='teacher_dashboard'),

    # Dashboard Stat Detail Pages
    path('stats/classes-today/', views.stat_classes_today, name='stat_classes_today'),
    path('stats/total-students/', views.stat_total_students, name='stat_total_students'),
    path('stats/pending-submissions/', views.stat_pending_submissions, name='stat_pending_submissions'),
    path('stats/leave-balance/', views.stat_leave_balance, name='stat_leave_balance'),

    # Attendance
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),
    path('attendance/absentee/', views.attendance_absentee, name='attendance_absentee'),

    # Marks Entry
    path('marks/add/', views.marks_add, name='marks_add'),
    path('marks/results/', views.marks_results, name='marks_results'),
    path('marks/report/', views.marks_report, name='marks_report'),
    
    # Class Tests
    path('class-tests/', views.class_test_list, name='class_test_list'),
    path('class-tests/<int:test_id>/edit/', views.class_test_edit, name='class_test_edit'),
    path('class-tests/<int:test_id>/delete/', views.class_test_delete, name='class_test_delete'),
    path('class-tests/<int:test_id>/toggle-publish/', views.class_test_toggle_publish, name='class_test_toggle_publish'),

    # My Schedule
    path('schedule/today/', views.today_routine, name='today_routine'),
    path('schedule/weekly/', views.weekly_timetable, name='weekly_timetable'),
    path('schedule/proxy/', views.proxy_classes, name='proxy_classes'),

    # Assignments
    path('assignments/create/', views.create_assignment, name='create_assignment'),
    path('assignments/review/', views.review_submissions, name='review_submissions'),
    path('assignments/study-material/', views.study_material, name='study_material'),

    # Online Classes
    path('online-classes/', views.online_classes, name='online_classes'),

    # Student Messages
    path('messages/', views.student_messages, name='student_messages'),
    path('messages/chat/', views.chat_student, name='chat_student'),

    # Payroll & HR
    path('hr/salary-slips/', views.salary_slips, name='salary_slips'),
    path('hr/leave-request/', views.leave_request, name='leave_request'),
    path('hr/profile/', views.my_profile, name='my_profile'),

    # Homework Upload
    path('homework/upload/', views.upload_homework, name='upload_homework'),
    path('homework/delete/<int:hw_id>/', views.delete_homework, name='delete_homework'),
]
