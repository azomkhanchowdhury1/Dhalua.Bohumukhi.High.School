from django.shortcuts import render
from django.db.models import Q
from .models import Notice

# START: NOTICE_VIEWS
def notice_list(request):
    """
    View to list notices based on public status and user roles.
    - Public notices: Everyone can see.
    - Role-based notices: Only specific roles can see (Student, Teacher, Staff, Parent).
    - Multi-role notices: Multiple roles can see.
    """
    if request.user.is_authenticated:
        # We determine the role. We can use the same logic as the context processor 
        # or use the context processor's global_role if available (but better to be explicit here).
        user = request.user
        role = "Admin" if user.is_superuser else "User"
        
        if hasattr(user, 'student_profile'):
            role = "Student"
        elif hasattr(user, 'teacher_profile'):
            role = "Teacher"
        elif hasattr(user, 'staff_profile'):
            role = "Staff"
        elif hasattr(user, 'parent_profile'):
            role = "Parent"
            
        # Admin can see everything
        if user.is_superuser or role == "Admin":
            notices = Notice.objects.all()
        else:
            # Filter: Public OR Target Role match
            query = Q(is_public=True)
            
            if role == 'Student':
                query |= Q(target_student=True)
            elif role == 'Teacher':
                query |= Q(target_teacher=True)
            elif role == 'Staff':
                query |= Q(target_staff=True)
            elif role == 'Parent':
                query |= Q(target_parent=True)
                
            notices = Notice.objects.filter(query).distinct()
    else:
        # Anonymous users only see public notices
        notices = Notice.objects.filter(is_public=True)
        
    return render(request, 'notices/notice_list.html', {'notices': notices})
# END: NOTICE_VIEWS
