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
    # START: EXAM_CRUD_URLS
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:exam_id>/edit/', views.exam_edit, name='exam_edit'),
    path('exams/<int:exam_id>/delete/', views.exam_delete, name='exam_delete'),
    # END: EXAM_CRUD_URLS
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
    # START: GALLERY_MANAGEMENT_URLS
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/<int:item_id>/edit/', views.gallery_edit, name='gallery_edit'),
    path('gallery/<int:item_id>/delete/', views.gallery_delete, name='gallery_delete'),
    path('gallery/<int:item_id>/toggle-remember/', views.gallery_toggle_remember, name='gallery_toggle_remember'),
    # END: GALLERY_MANAGEMENT_URLS
    
    # START: NOTICE_MANAGEMENT_URLS
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.notice_add, name='notice_add'),
    path('notices/<int:notice_id>/edit/', views.notice_edit, name='notice_edit'),
    path('notices/<int:notice_id>/delete/', views.notice_delete, name='notice_delete'),
    path('notices/<int:notice_id>/toggle-remember/', views.notice_toggle_remember, name='notice_toggle_remember'),
    # END: NOTICE_MANAGEMENT_URLS
    # START: STAFF_MANAGEMENT_URLS
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_add, name='staff_add'),
    path('staff/<int:staff_id>/edit/', views.staff_edit, name='staff_edit'),
    path('staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),
    # END: STAFF_MANAGEMENT_URLS
    
    # START: PARENT_MANAGEMENT_URLS
    path('parents/', views.parent_list, name='parent_list'),
    path('parents/add/', views.parent_add, name='parent_add'),
    path('parents/<int:parent_id>/edit/', views.parent_edit, name='parent_edit'),
    path('parents/<int:parent_id>/delete/', views.parent_delete, name='parent_delete'),
    # END: PARENT_MANAGEMENT_URLS

    # START: ACCOUNTS_MANAGEMENT_URLS
    path('accounts/registration-requests/', views.registration_requests, name='registration_requests'),
    path('accounts/registration-requests/<int:req_id>/edit/', views.registration_requests_edit, name='registration_requests_edit'),
    path('accounts/registration-requests/<int:req_id>/delete/', views.registration_requests_delete, name='registration_requests_delete'),
    path('accounts/registration-requests/<int:req_id>/toggle-remember/', views.registration_requests_toggle_remember, name='registration_requests_toggle_remember'),
    
    path('accounts/user-profiles/', views.user_profiles, name='user_profiles'),
    path('accounts/user-profiles/add/', views.user_profiles_add, name='user_profiles_add'),
    path('accounts/user-profiles/<int:profile_id>/edit/', views.user_profiles_edit, name='user_profiles_edit'),
    path('accounts/user-profiles/<int:profile_id>/delete/', views.user_profiles_delete, name='user_profiles_delete'),
    path('accounts/user-profiles/<int:profile_id>/toggle-remember/', views.user_profiles_toggle_remember, name='user_profiles_toggle_remember'),
    # END: ACCOUNTS_MANAGEMENT_URLS

    # START: AUTH_MANAGEMENT_URLS
    path('auth/groups/', views.auth_groups, name='auth_groups'),
    path('auth/groups/add/', views.auth_groups_add, name='auth_groups_add'),
    path('auth/groups/<int:group_id>/edit/', views.auth_groups_edit, name='auth_groups_edit'),
    path('auth/groups/<int:group_id>/delete/', views.auth_groups_delete, name='auth_groups_delete'),
    
    path('auth/users/', views.auth_users, name='auth_users'),
    path('auth/users/add/', views.auth_users_add, name='auth_users_add'),
    path('auth/users/<int:user_id>/edit/', views.auth_users_edit, name='auth_users_edit'),
    path('auth/users/<int:user_id>/delete/', views.auth_users_delete, name='auth_users_delete'),
    path('auth/users/<int:user_id>/toggle-active/', views.auth_user_toggle_active, name='auth_user_toggle_active'),
    # END: AUTH_MANAGEMENT_URLS
    
    # START: EVENTS_MANAGEMENT_URLS
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:event_id>/toggle-remember/', views.event_toggle_remember, name='event_toggle_remember'),
    # END: EVENTS_MANAGEMENT_URLS
]
