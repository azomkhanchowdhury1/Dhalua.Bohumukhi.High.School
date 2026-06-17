from django.shortcuts import render, redirect, get_object_or_404
from notices.models import Notice
from django.db.models import Q
from .models import Parent
from student.models import Attendance
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

# START: ACADEMIC_PROGRESS_VIEWS
@login_required
def report_cards(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/report_cards.html', {'parent': parent})

@login_required
def performance_analytics(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/performance_analytics.html', {'parent': parent})

@login_required
def subject_syllabus(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/subject_syllabus.html', {'parent': parent})
# END: ACADEMIC_PROGRESS_VIEWS

# START: ATTENDANCE_VIEWS
@login_required
def monthly_summary(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/monthly_summary.html', {'parent': parent})

@login_required
def detailed_absence_log(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/detailed_absence_log.html', {'parent': parent})

@login_required
def leave_notification(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/leave_notification.html', {'parent': parent})
# END: ATTENDANCE_VIEWS

# START: FINANCE_VIEWS
@login_required
def pay_online(request):
    from finance.models import FeeType, FeePayment
    parent = get_object_or_404(Parent, user=request.user)
    fee_types = FeeType.objects.all()

    if request.method == 'POST':
        fee_type_id = request.POST.get('fee_type')
        amount = request.POST.get('amount')
        txn_id = request.POST.get('transaction_id')
        student = parent.linked_student

        if not student:
            messages.error(request, 'কোনো ছাত্র/ছাত্রী লিঙ্ক করা নেই। অ্যাডমিনকে জানান।')
            return redirect('prents:pay_online')

        fee_type = get_object_or_404(FeeType, id=fee_type_id)

        if FeePayment.objects.filter(transaction_id=txn_id).exists():
            messages.error(request, 'এই ট্র্যানজেকশন আইডি ইতিমধ্যে ব্যবহার হয়েছে। আবার চেক করুন।')
        else:
            FeePayment.objects.create(
                student=student,
                fee_type=fee_type,
                amount_paid=amount,
                transaction_id=txn_id,
                status='Paid'
            )
            messages.success(request, f'৳{amount} পেমেন্ট সফলভাবে সাবমিট হয়েছে! TXN: {txn_id}')
            return redirect('prents:payment_receipts')

    return render(request, 'prents/pay_online.html', {
        'parent': parent,
        'fee_types': fee_types,
    })

@login_required
def payment_receipts(request):
    from finance.models import FeePayment
    parent = get_object_or_404(Parent, user=request.user)
    payments = []
    if parent.linked_student:
        payments = FeePayment.objects.filter(student=parent.linked_student).select_related('fee_type').order_by('-payment_date')
    return render(request, 'prents/payment_receipts.html', {
        'parent': parent,
        'payments': payments,
    })

@login_required
def fee_structure(request):
    from finance.models import FeeType
    parent = get_object_or_404(Parent, user=request.user)
    fee_types = FeeType.objects.all()
    total = sum(f.amount for f in fee_types)
    return render(request, 'prents/fee_structure.html', {
        'parent': parent,
        'fee_types': fee_types,
        'total': total,
    })
# END: FINANCE_VIEWS

# START: EXAMS_VIEWS
@login_required
def exam_schedule(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/exam_schedule.html', {'parent': parent})

@login_required
def class_timetable(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/class_timetable.html', {'parent': parent})

@login_required
def download_admit_card(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/download_admit_card.html', {'parent': parent})
# END: EXAMS_VIEWS

# START: SCHOOL_INFO_VIEWS
@login_required
def academic_calendar(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/academic_calendar.html', {'parent': parent})

@login_required
def transport_status(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/transport_status.html', {'parent': parent})

@login_required
def canteen_menu(request):
    parent = get_object_or_404(Parent, user=request.user)
    return render(request, 'prents/canteen_menu.html', {'parent': parent})
# END: SCHOOL_INFO_VIEWS
