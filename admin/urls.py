from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Student Management
    path('students/', views.student_list, name='student_list'),
    path('students/admission/', views.student_admission, name='student_admission'),
    path('students/attendance/', views.student_attendance, name='student_attendance'),
    path('students/promote/', views.student_promotion, name='student_promotion'),
    
    # Teacher Management
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/<int:teacher_id>/detail/', views.teacher_detail, name='teacher_detail'),
    path('teachers/<int:teacher_id>/edit/', views.teacher_edit, name='teacher_edit'),
    path('teachers/<int:teacher_id>/delete/', views.teacher_delete, name='teacher_delete'),
    path('teachers/<int:teacher_id>/toggle-active/', views.teacher_toggle_active, name='teacher_toggle_active'),
    path('teachers/<int:teacher_id>/reset-password/', views.teacher_reset_password, name='teacher_reset_password'),
    path('teachers/salary/', views.teacher_salary, name='teacher_salary'),
    path('teachers/assignments/', views.teacher_assignments, name='teacher_assignments'),
    
    # Academics Management
    path('academics/classes/', views.academics_classes, name='academics_classes'),
    path('academics/classes/edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('academics/classes/delete/<int:class_id>/', views.delete_class, name='delete_class'),
    path('academics/sections/edit/<int:section_id>/', views.edit_section, name='edit_section'),
    path('academics/sections/delete/<int:section_id>/', views.delete_section, name='delete_section'),
    path('academics/subjects/', views.academics_subjects, name='academics_subjects'),
    # START: SUBJECT_MANAGEMENT_URLS
    path('academics/subjects/<int:subject_id>/edit/', views.subject_edit, name='subject_edit'),
    path('academics/subjects/<int:subject_id>/delete/', views.subject_delete, name='subject_delete'),
    path('academics/subjects/<int:subject_id>/toggle-remember/', views.subject_toggle_remember, name='subject_toggle_remember'),
    # END: SUBJECT_MANAGEMENT_URLS
    path('academics/timetable/', views.academics_timetable, name='academics_timetable'),
    path('academics/timetable/<int:slot_id>/edit/', views.timetable_edit, name='timetable_edit'),
    path('academics/timetable/<int:slot_id>/delete/', views.timetable_delete, name='timetable_delete'),
    # START: TIMETABLE_TOGGLE_REMEMBER_URL
    path('academics/timetable/<int:slot_id>/toggle-remember/', views.timetable_toggle_remember, name='timetable_toggle_remember'),
    # END: TIMETABLE_TOGGLE_REMEMBER_URL
    path('academics/syllabus/', views.academics_syllabus, name='academics_syllabus'),
    # START: SYLLABUS_MANAGEMENT_URLS
    path('academics/syllabus/<int:syllabus_id>/edit/', views.syllabus_edit, name='syllabus_edit'),
    path('academics/syllabus/<int:syllabus_id>/delete/', views.syllabus_delete, name='syllabus_delete'),
    path('academics/syllabus/<int:syllabus_id>/toggle-remember/', views.syllabus_toggle_remember, name='syllabus_toggle_remember'),
    # END: SYLLABUS_MANAGEMENT_URLS
    
    # Exam Management
    path('exams/schedule/', views.exam_schedule, name='exam_schedule'),
    path('exams/schedule/<int:schedule_id>/edit/', views.exam_schedule_edit, name='exam_schedule_edit'),
    path('exams/schedule/<int:schedule_id>/delete/', views.exam_schedule_delete, name='exam_schedule_delete'),
    path('exams/schedule/<int:schedule_id>/toggle-remember/', views.exam_schedule_toggle_remember, name='exam_schedule_toggle_remember'),
    
    path('exams/marks-entry/', views.exam_marks_entry, name='exam_marks_entry'),
    
    path('exams/results/', views.exam_results, name='exam_results'),
    path('exams/results/<int:result_id>/edit/', views.exam_result_edit, name='exam_result_edit'),
    path('exams/results/<int:result_id>/delete/', views.exam_result_delete, name='exam_result_delete'),
    path('exams/results/<int:result_id>/toggle-remember/', views.exam_result_toggle_remember, name='exam_result_toggle_remember'),
    
    path('exams/grading/', views.exam_grading, name='exam_grading'),
    path('exams/grading/<int:grade_id>/edit/', views.exam_grading_edit, name='exam_grading_edit'),
    path('exams/grading/<int:grade_id>/delete/', views.exam_grading_delete, name='exam_grading_delete'),
    path('exams/grading/<int:grade_id>/toggle-remember/', views.exam_grading_toggle_remember, name='exam_grading_toggle_remember'),
    
    # Finance Management
    # START: FINANCE_MANAGEMENT_URLS
    path('finance/fees/', views.finance_fees, name='finance_fees'),
    path('finance/fee-type/<int:fee_type_id>/edit/', views.fee_type_edit, name='fee_type_edit'),
    path('finance/fee-type/<int:fee_type_id>/delete/', views.fee_type_delete, name='fee_type_delete'),
    path('finance/fee-type/<int:fee_type_id>/toggle-remember/', views.fee_type_toggle_remember, name='fee_type_toggle_remember'),
    path('finance/payment/<int:payment_id>/edit/', views.payment_edit, name='payment_edit'),
    path('finance/payment/<int:payment_id>/delete/', views.payment_delete, name='payment_delete'),
    path('finance/payment/<int:payment_id>/toggle-remember/', views.payment_toggle_remember, name='payment_toggle_remember'),
    path('finance/expenses/', views.finance_expenses, name='finance_expenses'),
    path('finance/expense/<int:expense_id>/edit/', views.expense_edit, name='expense_edit'),
    path('finance/expense/<int:expense_id>/delete/', views.expense_delete, name='expense_delete'),
    path('finance/expense/<int:expense_id>/toggle-remember/', views.expense_toggle_remember, name='expense_toggle_remember'),
    path('finance/history/', views.finance_history, name='finance_history'),
    path('finance/reports/', views.finance_reports, name='finance_reports'),
    # END: FINANCE_MANAGEMENT_URLS
]
