from django.shortcuts import render
from notices.models import Notice
from django.db.models import Q

# START: STAFF_VIEWS
def dashboard(request):
    # Fetch notices for staff
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_staff=True)).distinct().order_by('-created_at')[:5]
    return render(request, 'staff/dashboard.html', {'notices': notices})
# END: STAFF_VIEWS
