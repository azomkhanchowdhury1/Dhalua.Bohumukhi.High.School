from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, StudentActivityLog
from notices.models import Notice
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from academics.models import Timetable, Syllabus, Subject, SchoolClass
from teacher.models import Teacher, TeacherAssignment
from .models import StudentHomework, StudyMaterial, LibraryBook

@login_required
def dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_student=True)).distinct().order_by('-created_at')[:5]
    return render(request, 'student/dashboard.html', {'notices': notices, 'student': student})

@login_required
def academic_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    # Filter timetable by the student's current class name through the section relation
    timetable = Timetable.objects.filter(section__school_class__name=student.current_class).order_by('day', 'start_time')
    return render(request, 'student/timetable.html', {'timetable': timetable, 'student': student})

@login_required
def academic_syllabus(request):
    student = get_object_or_404(Student, user=request.user)
    # Filter syllabus by the student's current class name through the subject relation
    syllabus = Syllabus.objects.filter(subject__school_class__name=student.current_class).order_by('-uploaded_at')
    return render(request, 'student/syllabus.html', {'syllabus': syllabus, 'student': student})

@login_required
def academic_teachers(request):
    student = get_object_or_404(Student, user=request.user)
    # Fetch all teachers for now as there is no formal class assignment model yet
    teachers = Teacher.objects.all()
    return render(request, 'student/teachers.html', {'teachers': teachers, 'student': student})

@login_required
def academic_calendar(request):
    return render(request, 'student/calendar.html')

from exams.models import ExamSchedule, StudentResult, Exam, Grade

@login_required
def exam_routine(request):
    student = get_object_or_404(Student, user=request.user)
    schedules = ExamSchedule.objects.filter(school_class__name=student.current_class).select_related('exam', 'subject').order_by('date', 'start_time')
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

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        subject = request.POST.get('subject')
        file = request.FILES.get('file')
        StudentHomework.objects.create(
            student=student, title=title,
            description=description, subject=subject, file=file
        )
        StudentActivityLog.objects.create(
            student=student, action="Submitted Homework",
            details=f"Submitted homework: {title}"
        )
        messages.success(request, "Homework submitted successfully!")
        return redirect('student:learning_homework')

    return render(request, 'student/homework.html', {'homeworks': homeworks, 'student': student})

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
    return render(request, 'student/online_class.html')

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

