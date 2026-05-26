from django.shortcuts import render
from notices.models import Notice
from django.db.models import Q

# START: PARENT_VIEWS
def dashboard(request):
    # Fetch notices for parents
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_parent=True)).distinct().order_by('-created_at')[:5]
    return render(request, 'prents/dashboard.html', {'notices': notices})
# END: PARENT_VIEWS
