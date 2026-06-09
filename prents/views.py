from django.shortcuts import render, get_object_or_404
from notices.models import Notice
from django.db.models import Q
from .models import Parent
from student.models import Attendance
from django.contrib.auth.decorators import login_required

# START: PARENT_VIEWS
@login_required
def dashboard(request):
    parent = get_object_or_404(Parent, user=request.user)
    # Fetch notices for parents
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_parent=True)).distinct().order_by('-created_at')[:5]
    
    attendance_percentage = 0
    if parent.linked_student:
        total_records = Attendance.objects.filter(student=parent.linked_student, class_attendance__is_held=True).count()
        total_attended = Attendance.objects.filter(student=parent.linked_student, status='Present', class_attendance__is_held=True).count()
        attendance_percentage = round((total_attended / total_records) * 100, 1) if total_records > 0 else 0

    return render(request, 'prents/dashboard.html', {
        'notices': notices,
        'parent': parent,
        'attendance_percentage': attendance_percentage
    })
# END: PARENT_VIEWS
