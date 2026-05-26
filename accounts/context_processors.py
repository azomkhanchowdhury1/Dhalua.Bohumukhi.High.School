# START: ACCOUNTS_CONTEXT_PROCESSOR
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from prents.models import Parent

def user_profile_context(request):
    if request.user.is_authenticated:
        user = request.user
        role = "Admin" if user.is_superuser else "User"
        profile = None

        if hasattr(user, 'student_profile'):
            role = "Student"
            profile = user.student_profile
        elif hasattr(user, 'teacher_profile'):
            role = "Teacher"
            profile = user.teacher_profile
        elif hasattr(user, 'staff_profile'):
            role = "Staff"
            profile = user.staff_profile
        elif hasattr(user, 'parent_profile'):
            role = "Parent"
            profile = user.parent_profile
        
        return {
            'global_role': role,
            'global_profile': profile
        }
    return {}
# END: ACCOUNTS_CONTEXT_PROCESSOR
