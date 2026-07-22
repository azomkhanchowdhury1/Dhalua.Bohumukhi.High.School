from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Student, StudentActivityLog, Attendance, ClassAttendance
from notices.models import Notice
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from academics.models import Timetable, Syllabus, Subject, SchoolClass
from teacher.models import Teacher, TeacherAssignment
from .models import StudentHomework, StudyMaterial, LibraryBook

def _get_school_class(current_class_str):
    """Robust SchoolClass lookup — handles exact, icontains, and numeric variants."""
    if not current_class_str:
        return None
    # 1. Exact match
    cls = SchoolClass.objects.filter(name=current_class_str).first()
    if cls:
        return cls
    # 2. Case-insensitive contains
    cls = SchoolClass.objects.filter(name__icontains=current_class_str).first()
    if cls:
        return cls
    # 3. Try stripping 'Class ' prefix and search for number/word
    stripped = current_class_str.replace('Class ', '').replace('class ', '').strip()
    cls = SchoolClass.objects.filter(
        Q(name__icontains=stripped) | Q(code__icontains=stripped)
    ).first()
    return cls


@login_required
def dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_student=True)).distinct().order_by('-created_at')[:5]

    # --- Attendance Rate (all subjects combined) ---
    total_records = Attendance.objects.filter(student=student, class_attendance__is_held=True).count()
    total_attended = Attendance.objects.filter(student=student, status='Present', class_attendance__is_held=True).count()
    attendance_percentage = round((total_attended / total_records) * 100, 1) if total_records > 0 else 0

    # --- Active Subjects (subjects for student's class) — use robust lookup ---
    school_class_obj = _get_school_class(student.current_class)
    active_subjects_count = Subject.objects.filter(school_class=school_class_obj).count() if school_class_obj else 0

    # --- Pending Homework (submitted homeworks = total, not really "pending", but we show submitted count) ---
    pending_homework_count = StudentHomework.objects.filter(student=student).count()

    # --- Last GPA: average grade point from latest exam results ---
    from exams.models import StudentResult, Exam
    last_exam = Exam.objects.order_by('-id').first()
    last_gpa = 0.0
    if last_exam:
        results = StudentResult.objects.filter(student=student, exam=last_exam).select_related('grade')
        points = [r.grade.point for r in results if r.grade]
        last_gpa = round(sum(float(p) for p in points) / len(points), 2) if points else 0.0

    return render(request, 'student/dashboard.html', {
        'notices': notices,
        'student': student,
        'attendance_percentage': attendance_percentage,
        'active_subjects_count': active_subjects_count,
        'pending_homework_count': pending_homework_count,
        'last_gpa': last_gpa,
    })

@login_required
def attendance_detail(request):
    """Per-subject attendance breakdown for the logged-in student."""
    student = get_object_or_404(Student, user=request.user)
    school_class_obj = SchoolClass.objects.filter(name=student.current_class).first()
    subjects = Subject.objects.filter(school_class=school_class_obj) if school_class_obj else []

    subject_data = []
    for subject in subjects:
        held = ClassAttendance.objects.filter(
            school_class=school_class_obj, subject=subject, is_held=True
        ).count()
        attended = Attendance.objects.filter(
            student=student,
            class_attendance__subject=subject,
            class_attendance__is_held=True,
            status='Present'
        ).count()
        pct = round((attended / held) * 100, 1) if held > 0 else 0
        subject_data.append({
            'subject': subject,
            'held': held,
            'attended': attended,
            'percentage': pct,
        })

    return render(request, 'student/attendance_detail.html', {
        'student': student,
        'subject_data': subject_data,
    })





@login_required
def academic_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    school_class_obj = _get_school_class(student.current_class)
    
    timetable_qs = Timetable.objects.none()
    if school_class_obj:
        timetable_qs = Timetable.objects.filter(section__school_class=school_class_obj)
        if student.section:
            timetable_qs = timetable_qs.filter(section__name__iexact=student.section)
            
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    routine_data = []
    
    for day in days:
        slots = list(timetable_qs.filter(day=day).order_by('start_time').select_related('subject', 'section'))
        padded_slots = slots[:6] + [None] * (6 - len(slots))
        routine_data.append({
            'day': day,
            'slots': padded_slots
        })
        
    return render(request, 'student/timetable.html', {
        'routine_data': routine_data, 
        'student': student,
        'days': days,
    })

@login_required
def academic_syllabus(request):
    student = get_object_or_404(Student, user=request.user)
    school_class_obj = _get_school_class(student.current_class)
    if school_class_obj:
        syllabus = Syllabus.objects.filter(
            subject__school_class=school_class_obj
        ).order_by('-uploaded_at')
    else:
        syllabus = Syllabus.objects.none()
    return render(request, 'student/syllabus.html', {'syllabus': syllabus, 'student': student})

@login_required
def academic_teachers(request):
    student = get_object_or_404(Student, user=request.user)
    school_class_obj = _get_school_class(student.current_class)

    if school_class_obj:
        # 1st priority: teachers who have taken class via ClassAttendance
        teacher_ids = ClassAttendance.objects.filter(
            school_class=school_class_obj
        ).values_list('teacher_id', flat=True).distinct()
        teachers = Teacher.objects.filter(id__in=teacher_ids)
        # 2nd fallback: if no attendance records yet, show all teachers
        if not teachers.exists():
            teachers = Teacher.objects.all()
    else:
        # No class found at all — show all teachers so page isn't empty
        teachers = Teacher.objects.all()

    return render(request, 'student/teachers.html', {'teachers': teachers, 'student': student})

@login_required
def academic_calendar(request):
    return render(request, 'student/calendar.html')

from exams.models import ExamSchedule, StudentResult, Exam, Grade

@login_required
def exam_routine(request):
    student = get_object_or_404(Student, user=request.user)
    school_class = _get_school_class(student.current_class)
    if school_class:
        schedules = ExamSchedule.objects.filter(school_class=school_class).select_related('exam', 'subject').order_by('date', 'start_time')
    else:
        schedules = ExamSchedule.objects.none()
    return render(request, 'student/exam_routine.html', {'schedules': schedules, 'student': student})

@login_required
def exam_results(request):
    student = get_object_or_404(Student, user=request.user)
    results = StudentResult.objects.filter(student=student).select_related('exam', 'subject', 'grade').order_by('-exam__year')
    return render(request, 'student/results.html', {'results': results, 'student': student})

@login_required
def exam_analytics(request):
    student = get_object_or_404(Student, user=request.user)
    results = StudentResult.objects.filter(student=student).select_related('subject')
    
    # Calculate basic analytics
    total_marks = sum(r.marks_obtained for r in results)
    count = results.count()
    average = total_marks / count if count > 0 else 0
    
    return render(request, 'student/analytics.html', {
        'results': results,
        'average': average,
        'student': student
    })

@login_required
def exam_admit_card(request):
    student = get_object_or_404(Student, user=request.user)
    active_exams = Exam.objects.filter(is_active=True)
    return render(request, 'student/admit_card.html', {
        'student': student,
        'active_exams': active_exams
    })

@login_required
def profile(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'student/profile.html', {'student': student})

@login_required
def edit_profile(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        # Update user fields
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.save()
        
        # Update student fields
        student.phone_number = request.POST.get('phone')
        student.address = request.POST.get('address')
        student.blood_group = request.POST.get('blood_group')
        if request.FILES.get('profile_image'):
            student.profile_image = request.FILES.get('profile_image')
        student.save()
        
        # Log activity
        StudentActivityLog.objects.create(
            student=student,
            action="Updated Profile",
            details="Changed personal information and/or profile picture."
        )
        
        messages.success(request, "Profile updated successfully!")
        return redirect('student:profile')
    return render(request, 'student/edit_profile.html', {'student': student})

@login_required
def activity_log(request):
    student = get_object_or_404(Student, user=request.user)
    logs = StudentActivityLog.objects.filter(student=student).order_by('-timestamp')
    return render(request, 'student/activity_log.html', {'logs': logs})

# --- Learning Tools Views ---
@login_required
def learning_homework(request):
    student = get_object_or_404(Student, user=request.user)
    homeworks = StudentHomework.objects.filter(student=student).order_by('-submitted_at')
    teachers = Teacher.objects.select_related('user').all().order_by('user__first_name')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        subject = request.POST.get('subject')
        teacher_id = request.POST.get('teacher_id')
        file = request.FILES.get('file')
        
        teacher = get_object_or_404(Teacher, id=teacher_id) if teacher_id else None

        StudentHomework.objects.create(
            student=student, title=title,
            description=description, subject=subject, file=file,
            teacher=teacher
        )
        StudentActivityLog.objects.create(
            student=student, action="Submitted Homework",
            details=f"Submitted homework: {title} to {teacher.user.get_full_name() if teacher else 'None'}"
        )
        messages.success(request, "Homework submitted successfully!")
        return redirect('student:learning_homework')

    return render(request, 'student/homework.html', {
        'homeworks': homeworks, 
        'student': student,
        'teachers': teachers
    })

@login_required
def learning_study_material(request):
    student = get_object_or_404(Student, user=request.user)
    materials = StudyMaterial.objects.filter(
        school_class__name=student.current_class
    ).order_by('-uploaded_at')
    return render(request, 'student/study_material.html', {'materials': materials, 'student': student})

@login_required
def learning_library(request):
    student = get_object_or_404(Student, user=request.user)
    books = LibraryBook.objects.all().order_by('title')
    return render(request, 'student/library.html', {'books': books, 'student': student})

@login_required
def learning_online_class(request):
    student = get_object_or_404(Student, user=request.user)
    school_class_obj = _get_school_class(student.current_class)
    from academics.models import OnlineClass
    
    if school_class_obj:
        live_classes = OnlineClass.objects.filter(school_class=school_class_obj, status='Live').order_by('start_time')
        scheduled_classes = OnlineClass.objects.filter(school_class=school_class_obj, status='Scheduled').order_by('start_time')
        recorded_classes = OnlineClass.objects.filter(school_class=school_class_obj, status='Recorded').order_by('-start_time')
    else:
        live_classes = OnlineClass.objects.filter(status='Live').order_by('start_time')
        scheduled_classes = OnlineClass.objects.filter(status='Scheduled').order_by('start_time')
        recorded_classes = OnlineClass.objects.filter(status='Recorded').order_by('-start_time')

    return render(request, 'online_classes.html', {
        'live_classes': live_classes,
        'scheduled_classes': scheduled_classes,
        'recorded_classes': recorded_classes,
        'is_teacher': False,
        'student': student,
    })

# --- Fees & Dues Views ---
from finance.models import FeeType, FeePayment

@login_required
def fees_pay(request):
    student = get_object_or_404(Student, user=request.user)
    fee_types = FeeType.objects.all()

    if request.method == 'POST':
        fee_type_id = request.POST.get('fee_type')
        amount = request.POST.get('amount')
        txn_id = request.POST.get('transaction_id')
        fee_type = get_object_or_404(FeeType, id=fee_type_id)

        if FeePayment.objects.filter(transaction_id=txn_id).exists():
            messages.error(request, "This Transaction ID already exists. Please check and try again.")
        else:
            FeePayment.objects.create(
                student=student, fee_type=fee_type,
                amount_paid=amount, transaction_id=txn_id, status='Paid'
            )
            StudentActivityLog.objects.create(
                student=student, action="Fee Submitted",
                details=f"Submitted {fee_type.name} payment of ৳{amount}. TXN: {txn_id}"
            )
            messages.success(request, f"Payment of ৳{amount} for {fee_type.name} submitted successfully!")
            return redirect('student:fees_history')

    return render(request, 'student/fees_pay.html', {'fee_types': fee_types, 'student': student})

@login_required
def fees_history(request):
    student = get_object_or_404(Student, user=request.user)
    payments = FeePayment.objects.filter(student=student).select_related('fee_type').order_by('-payment_date')
    total_paid = sum(p.amount_paid for p in payments)
    return render(request, 'student/fees_history.html', {
        'payments': payments,
        'total_paid': total_paid,
        'student': student
    })

@login_required
def fees_structure(request):
    fee_types = FeeType.objects.all()
    total = sum(f.amount for f in fee_types)
    return render(request, 'student/fees_structure.html', {
        'fee_types': fee_types,
        'total': total
    })

@login_required
def message_teacher(request):
    from staff.models import DirectMessage
    teacher_id = request.GET.get('teacher_id') or request.POST.get('teacher_id')
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_user = teacher.user

    if request.method == 'POST':
        import json
        msg_text = ""
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                msg_text = data.get('message', '').strip()
            else:
                msg_text = request.POST.get('message', '').strip()
        except Exception:
            msg_text = request.POST.get('message', '').strip()

        if msg_text:
            msg = DirectMessage.objects.create(
                sender=request.user,
                receiver=teacher_user,
                message=msg_text
            )
            return JsonResponse({
                'status': 'success',
                'message': {
                    'id': msg.id,
                    'sender': msg.sender.username,
                    'sender_name': msg.sender.get_full_name() or msg.sender.username,
                    'message': msg.message,
                    'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)

    # GET: fetch messages
    messages = DirectMessage.objects.filter(
        Q(sender=request.user, receiver=teacher_user) |
        Q(sender=teacher_user, receiver=request.user)
    ).order_by('created_at')

    msg_list = []
    for msg in messages:
        msg_list.append({
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%d %b %Y, %I:%M %p')
        })

    # Mark as read
    DirectMessage.objects.filter(sender=teacher_user, receiver=request.user, is_read=False).update(is_read=True)

    return JsonResponse({
        'status': 'success',
        'messages': msg_list,
        'current_user_id': request.user.id
    })

