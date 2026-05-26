from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('dashboard/', views.dashboard, name='teacher_dashboard'),

    # Attendance
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
    path('attendance/history/', views.attendance_history, name='attendance_history'),
    path('attendance/absentee/', views.attendance_absentee, name='attendance_absentee'),

    # Marks Entry
    path('marks/add/', views.marks_add, name='marks_add'),
    path('marks/results/', views.marks_results, name='marks_results'),
    path('marks/report/', views.marks_report, name='marks_report'),
]
