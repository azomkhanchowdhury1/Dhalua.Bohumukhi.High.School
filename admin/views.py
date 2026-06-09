from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from student.models import Student, Attendance, PromotionHistory
from teacher.models import Teacher, SalaryPayment, TeacherAssignment
from academics.models import SchoolClass, Section, Subject, Timetable, Syllabus
from exams.models import Grade, Exam, ExamSchedule, StudentResult
from finance.models import FeeType, FeePayment, Expense
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from notices.models import Notice
from gallery.models import Gallery
from staff.models import Staff
from prents.models import Parent
from accounts.models import RegistrationRequest, UserProfile

# START: ADMIN_DASHBOARD_VIEWS
@staff_member_required
def dashboard(request):
    notices = Notice.objects.all().order_by('-created_at')[:5]
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_classes': SchoolClass.objects.count(),
        'notices': notices,
    }
    return render(request, 'admin/dashboard.html', context)

# --- Student Management Views ---
@staff_member_required
def student_list(request):
    query = request.GET.get('search', '')
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(student_id__icontains=query)
        )
    return render(request, 'admin/students/student_list.html', {'students': students, 'query': query})

@staff_member_required
def student_admission(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        current_class = request.POST.get('current_class')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            user = User.objects.create_user(username=student_id, email=email, password='password123')
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            Student.objects.create(
                user=user,
                student_id=student_id,
                current_class=current_class
            )
            messages.success(request, f"Student {first_name} admitted successfully!")
            return redirect('admin_panel:student_list')
    return render(request, 'admin/students/admission.html')

@staff_member_required
def student_attendance(request):
    query = request.GET.get('search', '')
    students = Student.objects.all()
    
    if query:
        students = students.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(student_id__icontains=query)
        )
    
    student_data = []
    for student in students:
        total_records = Attendance.objects.filter(student=student, class_attendance__is_held=True).count()
        total_attended = Attendance.objects.filter(student=student, status='Present', class_attendance__is_held=True).count()
        percentage = round((total_attended / total_records) * 100, 1) if total_records > 0 else 0
        student_data.append({
            'student': student,
            'percentage': percentage,
            'total_attended': total_attended,
            'total_classes': total_records
        })
        
    return render(request, 'admin/students/attendance.html', {
        'student_data': student_data,
        'query': query
    })

@staff_member_required
def student_promotion(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        to_class = request.POST.get('to_class')
        for sid in student_ids:
            student = get_object_or_404(Student, id=sid)
            old_class = student.current_class
            student.current_class = to_class
            student.save()
            
            PromotionHistory.objects.create(
                student=student,
                from_class=old_class,
                to_class=to_class,
                from_year="2023",
                to_year="2024"
            )
        messages.success(request, f"Selected students promoted to {to_class}!")
        return redirect('admin_panel:student_list')
    students = Student.objects.all()
    return render(request, 'admin/students/promotion.html', {'students': students})

# --- Teacher Management Views ---
@staff_member_required
def teacher_list(request):
    query = request.GET.get('search', '')
    teachers = Teacher.objects.all()
    if query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(teacher_id__icontains=query) |
            Q(department__icontains=query)
        )
    return render(request, 'admin/teachers/teacher_list.html', {'teachers': teachers, 'query': query})

@staff_member_required
def teacher_add(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        teacher_id = request.POST.get('teacher_id')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        subject = request.POST.get('subject', '')
        qualification = request.POST.get('qualification', '')
        joining_date = request.POST.get('joining_date') or None
        phone_number = request.POST.get('phone_number', '')
        gender = request.POST.get('gender', '')
        blood_group = request.POST.get('blood_group', '')
        address = request.POST.get('address', '')
        experience = request.POST.get('experience', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, "এই Email ইতিমধ্যে ব্যবহৃত হচ্ছে!")
        elif Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, "এই Teacher ID ইতিমধ্যে ব্যবহৃত হচ্ছে!")
        else:
            user = User.objects.create_user(username=teacher_id, email=email, password='teacherpassword')
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            Teacher.objects.create(
                user=user,
                teacher_id=teacher_id,
                department=department,
                salary=salary,
                subject=subject,
                qualification=qualification,
                joining_date=joining_date,
                phone_number=phone_number or None,
                gender=gender,
                blood_group=blood_group,
                address=address,
                experience=experience,
            )
            messages.success(request, f"শিক্ষক {first_name} {last_name} সফলভাবে যোগ করা হয়েছে!")
            return redirect('admin_panel:teacher_list')
    return render(request, 'admin/teachers/add_teacher.html')

@staff_member_required
def teacher_salary(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        year = request.POST.get('year')
        
        teacher = get_object_or_404(Teacher, id=teacher_id)
        SalaryPayment.objects.create(
            teacher=teacher,
            amount=amount,
            month=month,
            year=year,
            status='Paid'
        )
        messages.success(request, f"Salary payment for {teacher.user.first_name} recorded!")
    payments = SalaryPayment.objects.all().order_by('-payment_date')[:10]
    return render(request, 'admin/teachers/salary_management.html', {'teachers': teachers, 'payments': payments})

@staff_member_required
def teacher_assignments(request):
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        title = request.POST.get('title')
        desc = request.POST.get('description')
        due = request.POST.get('due_date')
        
        teacher = get_object_or_404(Teacher, id=teacher_id)
        TeacherAssignment.objects.create(
            teacher=teacher,
            title=title,
            description=desc,
            due_date=due
        )
        messages.success(request, "Assignment assigned to teacher!")
    assignments = TeacherAssignment.objects.all().order_by('-assigned_at')
    return render(request, 'admin/teachers/assignments.html', {'teachers': teachers, 'assignments': assignments})

@staff_member_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    salary_payments = SalaryPayment.objects.filter(teacher=teacher).order_by('-payment_date')
    assignments = TeacherAssignment.objects.filter(teacher=teacher).order_by('-assigned_at')
    return render(request, 'admin/teachers/teacher_detail.html', {
        'teacher': teacher,
        'salary_payments': salary_payments,
        'assignments': assignments,
    })

@staff_member_required
def teacher_edit(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        # User fields
        teacher.user.first_name = request.POST.get('first_name', teacher.user.first_name)
        teacher.user.last_name = request.POST.get('last_name', teacher.user.last_name)
        new_email = request.POST.get('email', teacher.user.email)
        if new_email != teacher.user.email and User.objects.filter(email=new_email).exclude(id=teacher.user.id).exists():
            messages.error(request, "এই Email ইতিমধ্যে অন্য অ্যাকাউন্টে ব্যবহৃত হচ্ছে!")
            return render(request, 'admin/teachers/teacher_edit.html', {'teacher': teacher})
        teacher.user.email = new_email
        teacher.user.save()

        # Teacher profile fields
        teacher.department = request.POST.get('department', teacher.department)
        teacher.subject = request.POST.get('subject', teacher.subject)
        teacher.qualification = request.POST.get('qualification', teacher.qualification)
        teacher.salary = request.POST.get('salary', teacher.salary)
        teacher.experience = request.POST.get('experience', teacher.experience)
        teacher.phone_number = request.POST.get('phone_number') or teacher.phone_number
        teacher.gender = request.POST.get('gender', teacher.gender)
        teacher.blood_group = request.POST.get('blood_group', teacher.blood_group)
        teacher.address = request.POST.get('address', teacher.address)
        joining = request.POST.get('joining_date')
        if joining:
            teacher.joining_date = joining

        # Profile image
        if request.FILES.get('profile_image'):
            teacher.profile_image = request.FILES['profile_image']

        teacher.save()
        messages.success(request, f"{teacher.user.get_full_name()} এর তথ্য সফলভাবে আপডেট করা হয়েছে!")
        return redirect('admin_panel:teacher_detail', teacher_id=teacher.id)
    return render(request, 'admin/teachers/teacher_edit.html', {'teacher': teacher})

@staff_member_required
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        name = teacher.user.get_full_name()
        user = teacher.user
        teacher.delete()
        user.delete()
        messages.success(request, f"শিক্ষক {name} সম্পূর্ণভাবে মুছে ফেলা হয়েছে!")
        return redirect('admin_panel:teacher_list')
    return render(request, 'admin/teachers/teacher_delete_confirm.html', {'teacher': teacher})

@staff_member_required
def teacher_toggle_active(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher.user.is_active = not teacher.user.is_active
    teacher.user.save()
    status = "সক্রিয়" if teacher.user.is_active else "নিষ্ক্রিয়"
    messages.success(request, f"{teacher.user.get_full_name()} এর অ্যাকাউন্ট {status} করা হয়েছে!")
    return redirect('admin_panel:teacher_list')

@staff_member_required
def teacher_reset_password(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password != confirm_password:
            messages.error(request, "পাসওয়ার্ড দুটো মিলছে না!")
        elif len(new_password) < 6:
            messages.error(request, "পাসওয়ার্ড কমপক্ষে ৬ অক্ষর হতে হবে!")
        else:
            teacher.user.set_password(new_password)
            teacher.user.save()
            messages.success(request, f"{teacher.user.get_full_name()} এর পাসওয়ার্ড সফলভাবে পরিবর্তন করা হয়েছে!")
            return redirect('admin_panel:teacher_detail', teacher_id=teacher.id)
    return render(request, 'admin/teachers/teacher_reset_password.html', {'teacher': teacher})

# --- Academics Management Views ---
@staff_member_required
def academics_classes(request):
    if request.method == 'POST':
        if 'add_class' in request.POST:
            name = request.POST.get('name')
            code = request.POST.get('code')
            if SchoolClass.objects.filter(code=code).exists():
                messages.error(request, f"Class code '{code}' already exists! Class codes must be unique.")
            else:
                SchoolClass.objects.create(name=name, code=code)
                messages.success(request, f"Class {name} added!")
        elif 'add_section' in request.POST:
            class_id = request.POST.get('class_id')
            name = request.POST.get('name')
            room = request.POST.get('room')
            school_class = get_object_or_404(SchoolClass, id=class_id)
            Section.objects.create(school_class=school_class, name=name, room_number=room)
            messages.success(request, f"Section {name} added to {school_class.name}!")
            
    classes = SchoolClass.objects.all().prefetch_related('sections')
    return render(request, 'admin/academics/classes.html', {'classes': classes})

@staff_member_required
def edit_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        if SchoolClass.objects.filter(code=code).exclude(id=class_id).exists():
            messages.error(request, f"Class code '{code}' already exists! Class codes must be unique.")
        else:
            school_class.name = name
            school_class.code = code
            school_class.save()
            messages.success(request, f"Class {name} updated successfully!")
            return redirect('admin_panel:academics_classes')
            
    return render(request, 'admin/academics/edit_class.html', {'school_class': school_class})

@staff_member_required
def delete_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    name = school_class.name
    school_class.delete()
    messages.success(request, f"Class {name} deleted successfully!")
    return redirect('admin_panel:academics_classes')

@staff_member_required
def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    classes = SchoolClass.objects.all()
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        name = request.POST.get('name')
        room = request.POST.get('room')
        school_class = get_object_or_404(SchoolClass, id=class_id)
        
        section.school_class = school_class
        section.name = name
        section.room_number = room
        section.save()
        messages.success(request, f"Section {name} updated successfully!")
        return redirect('admin_panel:academics_classes')
        
    return render(request, 'admin/academics/edit_section.html', {'section': section, 'classes': classes})

@staff_member_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    name = section.name
    class_name = section.school_class.name
    section.delete()
    messages.success(request, f"Section {name} deleted from {class_name} successfully!")
    return redirect('admin_panel:academics_classes')

@staff_member_required
def academics_subjects(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        name = request.POST.get('name')
        code = request.POST.get('code')
        school_class = get_object_or_404(SchoolClass, id=class_id)
        Subject.objects.create(school_class=school_class, name=name, code=code)
        messages.success(request, f"Subject {name} added to {school_class.name}!")

    # Filter by class
    filter_class = request.GET.get('filter_class', '')
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all().select_related('school_class')
    if filter_class:
        subjects = subjects.filter(school_class_id=filter_class)
    subjects = subjects.order_by('school_class__name', 'name')
    return render(request, 'admin/academics/subjects.html', {
        'classes': classes,
        'subjects': subjects,
        'filter_class': filter_class,
    })

# START: SUBJECT_MANAGEMENT_VIEWS
@staff_member_required
def subject_edit(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    classes = SchoolClass.objects.all()

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        name = request.POST.get('name')
        code = request.POST.get('code')
        is_remembered = request.POST.get('is_remembered') == 'on'
        reminder_note = request.POST.get('reminder_note', '')

        school_class = get_object_or_404(SchoolClass, id=class_id)
        subject.school_class = school_class
        subject.name = name
        subject.code = code
        subject.is_remembered = is_remembered
        subject.reminder_note = reminder_note
        subject.save()
        messages.success(request, f"Subject '{name}' updated successfully!")
        return redirect('admin_panel:academics_subjects')

    return render(request, 'admin/academics/subject_edit.html', {
        'subject': subject,
        'classes': classes,
    })

@staff_member_required
def subject_delete(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject '{name}' deleted successfully!")
        return redirect('admin_panel:academics_subjects')
    return render(request, 'admin/academics/subject_delete_confirm.html', {'subject': subject})

@staff_member_required
def subject_toggle_remember(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.is_remembered = not subject.is_remembered
    subject.save()
    status = "marked with reminder" if subject.is_remembered else "removed from reminders"
    messages.success(request, f"Subject '{subject.name}' has been {status}!")
    return redirect('admin_panel:academics_subjects')
# END: SUBJECT_MANAGEMENT_VIEWS

@staff_member_required
def academics_timetable(request):
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        day = request.POST.get('day')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')

        section = get_object_or_404(Section, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)

        # Duplicate check
        if Timetable.objects.filter(section=section, day=day, start_time=start).exists():
            messages.error(request, f"এই Section-এ {day}-তে {start} সময়ে ইতিমধ্যে একটি slot আছে!")
        else:
            Timetable.objects.create(section=section, subject=subject, day=day, start_time=start, end_time=end)
            messages.success(request, f"Timetable slot সফলভাবে যোগ করা হয়েছে!")
        return redirect('admin_panel:academics_timetable')

    sections = Section.objects.all().select_related('school_class')
    subjects = Subject.objects.all().select_related('school_class')
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Filter support
    filter_section = request.GET.get('filter_section', '')
    filter_day = request.GET.get('filter_day', '')

    timetables = Timetable.objects.all().select_related('section__school_class', 'subject')
    if filter_section:
        timetables = timetables.filter(section_id=filter_section)
    if filter_day:
        timetables = timetables.filter(day=filter_day)
    timetables = timetables.order_by('day', 'start_time')

    return render(request, 'admin/academics/timetable.html', {
        'sections': sections,
        'subjects': subjects,
        'timetables': timetables,
        'days': days,
        'filter_section': filter_section,
        'filter_day': filter_day,
    })

@staff_member_required
def timetable_edit(request, slot_id):
    slot = get_object_or_404(Timetable, id=slot_id)
    sections = Section.objects.all().select_related('school_class')
    subjects = Subject.objects.all().select_related('school_class')
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        day = request.POST.get('day')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')

        section = get_object_or_404(Section, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)

        # Duplicate check (exclude self)
        if Timetable.objects.filter(section=section, day=day, start_time=start).exclude(id=slot_id).exists():
            messages.error(request, f"এই Section-এ {day}-তে {start} সময়ে ইতিমধ্যে অন্য একটি slot আছে!")
        else:
            slot.section = section
            slot.subject = subject
            slot.day = day
            slot.start_time = start
            slot.end_time = end
            # START: TIMETABLE_REMINDER_EDIT_LOGIC
            slot.is_remembered = request.POST.get('is_remembered') == 'on'
            slot.reminder_note = request.POST.get('reminder_note', '')
            # END: TIMETABLE_REMINDER_EDIT_LOGIC
            slot.save()
            messages.success(request, "Timetable slot সফলভাবে আপডেট করা হয়েছে!")
            return redirect('admin_panel:academics_timetable')

    return render(request, 'admin/academics/timetable_edit.html', {
        'slot': slot,
        'sections': sections,
        'subjects': subjects,
        'days': days,
    })

# START: TIMETABLE_TOGGLE_REMEMBER_VIEW
@staff_member_required
def timetable_toggle_remember(request, slot_id):
    slot = get_object_or_404(Timetable, id=slot_id)
    slot.is_remembered = not slot.is_remembered
    slot.save()
    status = "marked with reminder" if slot.is_remembered else "removed from reminders"
    messages.success(request, f"Timetable slot for {slot.subject.name} has been {status}!")
    return redirect('admin_panel:academics_timetable')
# END: TIMETABLE_TOGGLE_REMEMBER_VIEW

@staff_member_required
def timetable_delete(request, slot_id):
    slot = get_object_or_404(Timetable, id=slot_id)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, "Timetable slot সফলভাবে মুছে ফেলা হয়েছে!")
        return redirect('admin_panel:academics_timetable')
    return render(request, 'admin/academics/timetable_delete_confirm.html', {'slot': slot})

@staff_member_required
def academics_syllabus(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        file = request.FILES.get('file')
        subject = get_object_or_404(Subject, id=subject_id)
        Syllabus.objects.create(subject=subject, title=title, file=file)
        messages.success(request, "Syllabus uploaded!")
        
    subjects = Subject.objects.all()
    syllabi = Syllabus.objects.all().select_related('subject')
    return render(request, 'admin/academics/syllabus.html', {'subjects': subjects, 'syllabi': syllabi})

# START: SYLLABUS_MANAGEMENT_VIEWS
@staff_member_required
def syllabus_edit(request, syllabus_id):
    syllabus = get_object_or_404(Syllabus, id=syllabus_id)
    subjects = Subject.objects.all()

    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        file = request.FILES.get('file')
        is_remembered = request.POST.get('is_remembered') == 'on'
        reminder_note = request.POST.get('reminder_note', '')

        subject = get_object_or_404(Subject, id=subject_id)
        syllabus.subject = subject
        syllabus.title = title
        if file:
            syllabus.file = file
        syllabus.is_remembered = is_remembered
        syllabus.reminder_note = reminder_note
        syllabus.save()
        messages.success(request, "Syllabus successfully updated!")
        return redirect('admin_panel:academics_syllabus')

    return render(request, 'admin/academics/syllabus_edit.html', {
        'syllabus': syllabus,
        'subjects': subjects,
    })

@staff_member_required
def syllabus_delete(request, syllabus_id):
    syllabus = get_object_or_404(Syllabus, id=syllabus_id)
    if request.method == 'POST':
        title = syllabus.title
        syllabus.delete()
        messages.success(request, f"Syllabus '{title}' deleted successfully!")
        return redirect('admin_panel:academics_syllabus')
    return render(request, 'admin/academics/syllabus_delete_confirm.html', {'syllabus': syllabus})

@staff_member_required
def syllabus_toggle_remember(request, syllabus_id):
    syllabus = get_object_or_404(Syllabus, id=syllabus_id)
    syllabus.is_remembered = not syllabus.is_remembered
    syllabus.save()
    status = "marked with reminder" if syllabus.is_remembered else "removed from reminders"
    messages.success(request, f"Syllabus for {syllabus.subject.name} has been {status}!")
    return redirect('admin_panel:academics_syllabus')
# END: SYLLABUS_MANAGEMENT_VIEWS

# --- Exam Management Views ---
# START: EXAM_CRUD_VIEWS
@staff_member_required
def exam_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        year = request.POST.get('year')
        is_active = request.POST.get('is_active') == 'on'
        
        Exam.objects.create(name=name, year=year, is_active=is_active)
        messages.success(request, f"Exam '{name}' added successfully!")
        return redirect('admin_panel:exam_list')
        
    exams = Exam.objects.all().order_by('-year', 'name')
    return render(request, 'admin/exams/exam_list.html', {'exams': exams})

@staff_member_required
def exam_edit(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        exam.name = request.POST.get('name')
        exam.year = request.POST.get('year')
        exam.is_active = request.POST.get('is_active') == 'on'
        exam.save()
        messages.success(request, f"Exam '{exam.name}' updated successfully!")
        return redirect('admin_panel:exam_list')
    return render(request, 'admin/exams/exam_edit.html', {'exam': exam})

@staff_member_required
def exam_delete(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        name = exam.name
        exam.delete()
        messages.success(request, f"Exam '{name}' deleted successfully!")
        return redirect('admin_panel:exam_list')
    return render(request, 'admin/exams/exam_delete_confirm.html', {'exam': exam})
# END: EXAM_CRUD_VIEWS

@staff_member_required
def exam_schedule(request):
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        time = request.POST.get('start_time')
        room = request.POST.get('room')
        
        exam = get_object_or_404(Exam, id=exam_id)
        s_class = get_object_or_404(SchoolClass, id=class_id)
        subject = get_object_or_404(Subject, id=subject_id)
        
        ExamSchedule.objects.create(
            exam=exam, school_class=s_class, subject=subject,
            date=date, start_time=time, room_number=room
        )
        messages.success(request, "Exam schedule added!")
        
    exams = Exam.objects.filter(is_active=True)
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()
    schedules = ExamSchedule.objects.all().select_related('exam', 'school_class', 'subject').order_by('date', 'start_time')
    return render(request, 'admin/exams/schedule.html', {
        'exams': exams, 'classes': classes, 'subjects': subjects, 'schedules': schedules
    })

@staff_member_required
def exam_schedule_edit(request, schedule_id):
    schedule = get_object_or_404(ExamSchedule, id=schedule_id)
    exams = Exam.objects.filter(is_active=True)
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()
    
    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        class_id = request.POST.get('class_id')
        subject_id = request.POST.get('subject_id')
        date = request.POST.get('date')
        time = request.POST.get('start_time')
        room = request.POST.get('room')
        is_remembered = request.POST.get('is_remembered') == 'on'
        reminder_note = request.POST.get('reminder_note', '')
        
        schedule.exam = get_object_or_404(Exam, id=exam_id)
        schedule.school_class = get_object_or_404(SchoolClass, id=class_id)
        schedule.subject = get_object_or_404(Subject, id=subject_id)
        schedule.date = date
        schedule.start_time = time
        schedule.room_number = room
        schedule.is_remembered = is_remembered
        schedule.reminder_note = reminder_note
        schedule.save()
        
        messages.success(request, "Exam schedule updated successfully!")
        return redirect('admin_panel:exam_schedule')
        
    return render(request, 'admin/exams/schedule_edit.html', {
        'schedule': schedule,
        'exams': exams,
        'classes': classes,
        'subjects': subjects,
    })

@staff_member_required
def exam_schedule_delete(request, schedule_id):
    schedule = get_object_or_404(ExamSchedule, id=schedule_id)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Exam schedule deleted successfully!")
        return redirect('admin_panel:exam_schedule')
    return render(request, 'admin/exams/schedule_delete_confirm.html', {'schedule': schedule})

@staff_member_required
def exam_schedule_toggle_remember(request, schedule_id):
    schedule = get_object_or_404(ExamSchedule, id=schedule_id)
    schedule.is_remembered = not schedule.is_remembered
    schedule.save()
    status = "marked with reminder" if schedule.is_remembered else "removed from reminders"
    messages.success(request, f"Exam schedule for {schedule.subject.name} has been {status}!")
    return redirect('admin_panel:exam_schedule')

@staff_member_required
def exam_marks_entry(request):
    classes = SchoolClass.objects.all()
    exams = Exam.objects.filter(is_active=True)
    subjects = Subject.objects.all()
    
    selected_class = request.GET.get('class')
    selected_exam = request.GET.get('exam')
    selected_subject = request.GET.get('subject')
    
    students = []
    if selected_class and selected_exam and selected_subject:
        s_class_obj = get_object_or_404(SchoolClass, id=selected_class)
        students = Student.objects.filter(current_class=s_class_obj.name)
        
        # Populate existing marks
        results_map = {
            r.student_id: r.marks_obtained 
            for r in StudentResult.objects.filter(exam_id=selected_exam, subject_id=selected_subject)
        }
        for student in students:
            student.existing_mark = results_map.get(student.id)
            
        if request.method == 'POST':
            for student in students:
                marks = request.POST.get(f'marks_{student.id}')
                if marks:
                    mark_int = int(marks)
                    grade_obj = Grade.objects.filter(min_mark__lte=mark_int, max_mark__gte=mark_int).first()
                    
                    StudentResult.objects.update_or_create(
                        student=student,
                        exam_id=selected_exam,
                        subject_id=selected_subject,
                        defaults={'marks_obtained': mark_int, 'grade': grade_obj}
                    )
            messages.success(request, "Marks updated successfully!")
            return redirect(f"{request.path}?class={selected_class}&exam={selected_exam}&subject={selected_subject}")
            
    return render(request, 'admin/exams/marks_entry.html', {
        'classes': classes, 'exams': exams, 'subjects': subjects, 'students': students,
        'selected_class': selected_class, 'selected_exam': selected_exam, 'selected_subject': selected_subject
    })

@staff_member_required
def exam_results(request):
    results = StudentResult.objects.all().select_related('student__user', 'exam', 'subject', 'grade').order_by('-id')
    return render(request, 'admin/exams/results.html', {'results': results})

@staff_member_required
def exam_result_edit(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    if request.method == 'POST':
        marks = request.POST.get('marks_obtained')
        remarks = request.POST.get('remarks', '')
        is_remembered = request.POST.get('is_remembered') == 'on'
        reminder_note = request.POST.get('reminder_note', '')
        
        if marks:
            mark_int = int(marks)
            grade_obj = Grade.objects.filter(min_mark__lte=mark_int, max_mark__gte=mark_int).first()
            result.marks_obtained = mark_int
            result.grade = grade_obj
        result.remarks = remarks
        result.is_remembered = is_remembered
        result.reminder_note = reminder_note
        result.save()
        
        messages.success(request, "Student result updated successfully!")
        return redirect('admin_panel:exam_results')
        
    return render(request, 'admin/exams/result_edit.html', {
        'result': result,
    })

@staff_member_required
def exam_result_delete(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, "Student result deleted successfully!")
        return redirect('admin_panel:exam_results')
    return render(request, 'admin/exams/result_delete_confirm.html', {'result': result})

@staff_member_required
def exam_result_toggle_remember(request, result_id):
    result = get_object_or_404(StudentResult, id=result_id)
    result.is_remembered = not result.is_remembered
    result.save()
    status = "marked with reminder" if result.is_remembered else "removed from reminders"
    messages.success(request, f"Result for {result.student.user.get_full_name()} has been {status}!")
    return redirect('admin_panel:exam_results')

@staff_member_required
def exam_grading(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        min_m = request.POST.get('min_mark')
        max_m = request.POST.get('max_mark')
        point = request.POST.get('point')
        
        Grade.objects.create(name=name, min_mark=min_m, max_mark=max_m, point=point)
        messages.success(request, f"Grade {name} added!")
        
    grades = Grade.objects.all().order_by('-point')
    return render(request, 'admin/exams/grading.html', {'grades': grades})

@staff_member_required
def exam_grading_edit(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        min_m = request.POST.get('min_mark')
        max_m = request.POST.get('max_mark')
        point = request.POST.get('point')
        is_remembered = request.POST.get('is_remembered') == 'on'
        reminder_note = request.POST.get('reminder_note', '')
        
        grade.name = name
        grade.min_mark = min_m
        grade.max_mark = max_m
        grade.point = point
        grade.is_remembered = is_remembered
        grade.reminder_note = reminder_note
        grade.save()
        
        messages.success(request, "Grade rule updated successfully!")
        return redirect('admin_panel:exam_grading')
        
    return render(request, 'admin/exams/grading_edit.html', {'grade': grade})

@staff_member_required
def exam_grading_delete(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, "Grade rule deleted successfully!")
        return redirect('admin_panel:exam_grading')
    return render(request, 'admin/exams/grading_delete_confirm.html', {'grade': grade})

@staff_member_required
def exam_grading_toggle_remember(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    grade.is_remembered = not grade.is_remembered
    grade.save()
    status = "marked with reminder" if grade.is_remembered else "removed from reminders"
    messages.success(request, f"Grade rule for {grade.name} has been {status}!")
    return redirect('admin_panel:exam_grading')

# --- Finance Management Views ---
@staff_member_required
def finance_fees(request):
    if request.method == 'POST':
        if 'add_fee_type' in request.POST:
            name = request.POST.get('name')
            amount = request.POST.get('amount')
            FeeType.objects.create(name=name, amount=amount)
            messages.success(request, f"Fee type '{name}' added successfully!")
        elif 'add_payment' in request.POST:
            student_id = request.POST.get('student_id')
            fee_type_id = request.POST.get('fee_type')
            amount = request.POST.get('amount')
            txn_id = request.POST.get('transaction_id')
            
            student = Student.objects.filter(student_id=student_id).first()
            if not student:
                messages.error(request, f"No student found with ID '{student_id}'. Please check the Student ID and try again.")
            else:
                fee_type = get_object_or_404(FeeType, id=fee_type_id)
                
                FeePayment.objects.create(
                    student=student, fee_type=fee_type,
                    amount_paid=amount, transaction_id=txn_id
                )
                messages.success(request, f"Fee payment of ${amount} received from {student.user.first_name}!")
        
        
    fee_types = FeeType.objects.all()
    recent_payments = FeePayment.objects.all().select_related('student', 'fee_type').order_by('-payment_date')
    return render(request, 'admin/finance/fees.html', {'fee_types': fee_types, 'recent_payments': recent_payments})

@staff_member_required
def finance_expenses(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        
        Expense.objects.create(title=title, category=category, amount=amount, date=date)
        messages.success(request, f"Expense '{title}' recorded!")
        
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'admin/finance/expenses.html', {'expenses': expenses})

@staff_member_required
def finance_history(request):
    payments = FeePayment.objects.all().select_related('student', 'fee_type').order_by('-payment_date')
    return render(request, 'admin/finance/history.html', {'payments': payments})

@staff_member_required
def finance_reports(request):
    from django.db.models import Sum
    total_fees = FeePayment.objects.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_fees - total_expenses
    
    return render(request, 'admin/finance/reports.html', {
        'total_fees': total_fees,
        'total_expenses': total_expenses,
        'balance': balance
    })

# START: FINANCE_FEE_TYPE_CRUD_VIEWS
@staff_member_required
def fee_type_edit(request, fee_type_id):
    fee_type = get_object_or_404(FeeType, id=fee_type_id)
    if request.method == 'POST':
        fee_type.name = request.POST.get('name', fee_type.name)
        fee_type.amount = request.POST.get('amount', fee_type.amount)
        fee_type.is_remembered = request.POST.get('is_remembered') == 'on'
        fee_type.reminder_note = request.POST.get('reminder_note', '')
        fee_type.save()
        messages.success(request, f"Fee type '{fee_type.name}' updated successfully!")
        return redirect('admin_panel:finance_fees')
    return render(request, 'admin/finance/fee_type_edit.html', {'fee_type': fee_type})

@staff_member_required
def fee_type_delete(request, fee_type_id):
    fee_type = get_object_or_404(FeeType, id=fee_type_id)
    if request.method == 'POST':
        name = fee_type.name
        fee_type.delete()
        messages.success(request, f"Fee type '{name}' deleted successfully!")
        return redirect('admin_panel:finance_fees')
    return render(request, 'admin/finance/fee_type_delete_confirm.html', {'fee_type': fee_type})

@staff_member_required
def fee_type_toggle_remember(request, fee_type_id):
    fee_type = get_object_or_404(FeeType, id=fee_type_id)
    fee_type.is_remembered = not fee_type.is_remembered
    fee_type.save()
    status = "marked with reminder" if fee_type.is_remembered else "removed from reminders"
    messages.success(request, f"Fee type '{fee_type.name}' has been {status}!")
    return redirect('admin_panel:finance_fees')
# END: FINANCE_FEE_TYPE_CRUD_VIEWS

# START: FINANCE_PAYMENT_CRUD_VIEWS
@staff_member_required
def payment_edit(request, payment_id):
    payment = get_object_or_404(FeePayment, id=payment_id)
    fee_types = FeeType.objects.all()
    if request.method == 'POST':
        fee_type_id = request.POST.get('fee_type')
        payment.fee_type = get_object_or_404(FeeType, id=fee_type_id)
        payment.amount_paid = request.POST.get('amount_paid', payment.amount_paid)
        payment.transaction_id = request.POST.get('transaction_id', payment.transaction_id)
        payment.status = request.POST.get('status', payment.status)
        payment.is_remembered = request.POST.get('is_remembered') == 'on'
        payment.reminder_note = request.POST.get('reminder_note', '')
        payment.save()
        messages.success(request, "Payment record updated successfully!")
        return redirect('admin_panel:finance_fees')
    return render(request, 'admin/finance/payment_edit.html', {'payment': payment, 'fee_types': fee_types})

@staff_member_required
def payment_delete(request, payment_id):
    payment = get_object_or_404(FeePayment, id=payment_id)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, "Payment record deleted successfully!")
        return redirect('admin_panel:finance_fees')
    return render(request, 'admin/finance/payment_delete_confirm.html', {'payment': payment})

@staff_member_required
def payment_toggle_remember(request, payment_id):
    payment = get_object_or_404(FeePayment, id=payment_id)
    payment.is_remembered = not payment.is_remembered
    payment.save()
    status = "marked with reminder" if payment.is_remembered else "removed from reminders"
    messages.success(request, f"Payment #{payment.transaction_id} has been {status}!")
    return redirect('admin_panel:finance_fees')
# END: FINANCE_PAYMENT_CRUD_VIEWS

# START: FINANCE_EXPENSE_CRUD_VIEWS
@staff_member_required
def expense_edit(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.title = request.POST.get('title', expense.title)
        expense.category = request.POST.get('category', expense.category)
        expense.amount = request.POST.get('amount', expense.amount)
        expense.date = request.POST.get('date', expense.date)
        expense.description = request.POST.get('description', '')
        expense.is_remembered = request.POST.get('is_remembered') == 'on'
        expense.reminder_note = request.POST.get('reminder_note', '')
        expense.save()
        messages.success(request, f"Expense '{expense.title}' updated successfully!")
        return redirect('admin_panel:finance_expenses')
    return render(request, 'admin/finance/expense_edit.html', {'expense': expense})

@staff_member_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        title = expense.title
        expense.delete()
        messages.success(request, f"Expense '{title}' deleted successfully!")
        return redirect('admin_panel:finance_expenses')
    return render(request, 'admin/finance/expense_delete_confirm.html', {'expense': expense})

@staff_member_required
def expense_toggle_remember(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.is_remembered = not expense.is_remembered
    expense.save()
    status = "marked with reminder" if expense.is_remembered else "removed from reminders"
    messages.success(request, f"Expense '{expense.title}' has been {status}!")
    return redirect('admin_panel:finance_expenses')
# END: FINANCE_EXPENSE_CRUD_VIEWS
# START: GALLERY_VIEWS
@staff_member_required
def gallery_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        file = request.FILES.get('file')
        if title and file and category:
            Gallery.objects.create(title=title, category=category, file=file)
            messages.success(request, f"Media '{title}' uploaded successfully!")
        return redirect('admin_panel:gallery_list')

    items = Gallery.objects.all().order_by('-created_at')
    return render(request, 'admin/gallery/gallery_list.html', {'items': items})

@staff_member_required
def gallery_delete(request, item_id):
    item = get_object_or_404(Gallery, id=item_id)
    if request.method == 'POST':
        if item.file:
            item.file.delete(save=False)
        item.delete()
        messages.success(request, "Media deleted successfully!")
        return redirect('admin_panel:gallery_list')
    return redirect('admin_panel:gallery_list')
# END: GALLERY_VIEWS

# START: NOTICE_VIEWS
@staff_member_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'admin/notices/notice_list.html', {'notices': notices})

@staff_member_required
def notice_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = request.POST.get('is_public') == 'on'
        target_student = request.POST.get('target_student') == 'on'
        target_teacher = request.POST.get('target_teacher') == 'on'
        target_staff = request.POST.get('target_staff') == 'on'
        target_parent = request.POST.get('target_parent') == 'on'
        signature = request.FILES.get('signature')
        attachment = request.FILES.get('attachment')
        
        Notice.objects.create(
            title=title, content=content, is_public=is_public,
            target_student=target_student, target_teacher=target_teacher,
            target_staff=target_staff, target_parent=target_parent,
            signature=signature, attachment=attachment,
            created_by=request.user
        )
        messages.success(request, "Notice created successfully!")
        return redirect('admin_panel:notice_list')
    return render(request, 'admin/notices/notice_edit.html')

@staff_member_required
def notice_edit(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.title = request.POST.get('title', notice.title)
        notice.content = request.POST.get('content', notice.content)
        notice.is_public = request.POST.get('is_public') == 'on'
        notice.target_student = request.POST.get('target_student') == 'on'
        notice.target_teacher = request.POST.get('target_teacher') == 'on'
        notice.target_staff = request.POST.get('target_staff') == 'on'
        notice.target_parent = request.POST.get('target_parent') == 'on'
        
        if 'signature' in request.FILES:
            notice.signature = request.FILES.get('signature')
        if 'attachment' in request.FILES:
            notice.attachment = request.FILES.get('attachment')
            
        notice.save()
        messages.success(request, "Notice updated successfully!")
        return redirect('admin_panel:notice_list')
    return render(request, 'admin/notices/notice_edit.html', {'notice': notice})

@staff_member_required
def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully!")
        return redirect('admin_panel:notice_list')
    return render(request, 'admin/notices/notice_delete_confirm.html', {'notice': notice})
# END: NOTICE_VIEWS

# START: STAFF_VIEWS
@staff_member_required
def staff_list(request):
    query = request.GET.get('search', '')
    staffs = Staff.objects.select_related('user').all()
    if query:
        staffs = staffs.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(staff_id__icontains=query) | Q(designation__icontains=query))
    return render(request, 'admin/staff/staff_list.html', {'staffs': staffs, 'search': query})

@staff_member_required
def staff_add(request):
    students = Student.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        salary = request.POST.get('salary') or None
        joining_date = request.POST.get('joining_date') or None
        work_shift = request.POST.get('work_shift')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already taken.")
            return redirect('admin_panel:staff_add')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_staff=True)
        staff_id = f"STF{user.id:04d}"
        profile_image = request.FILES.get('profile_image')
        Staff.objects.create(user=user, staff_id=staff_id, designation=designation, department=department, phone_number=phone_number, address=address, salary=salary, joining_date=joining_date, work_shift=work_shift, gender=gender, profile_image=profile_image)
        messages.success(request, f"Staff '{first_name} {last_name}' added successfully!")
        return redirect('admin_panel:staff_list')
    return render(request, 'admin/staff/staff_edit.html', {'mode': 'add'})

@staff_member_required
def staff_edit(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        staff.user.first_name = request.POST.get('first_name', staff.user.first_name)
        staff.user.last_name = request.POST.get('last_name', staff.user.last_name)
        staff.user.email = request.POST.get('email', staff.user.email)
        staff.user.save()
        staff.designation = request.POST.get('designation', staff.designation)
        staff.department = request.POST.get('department', staff.department)
        staff.phone_number = request.POST.get('phone_number', staff.phone_number)
        staff.address = request.POST.get('address', staff.address)
        staff.salary = request.POST.get('salary') or staff.salary
        staff.joining_date = request.POST.get('joining_date') or staff.joining_date
        staff.work_shift = request.POST.get('work_shift', staff.work_shift)
        staff.gender = request.POST.get('gender', staff.gender)
        if 'profile_image' in request.FILES:
            staff.profile_image = request.FILES['profile_image']
        staff.save()
        messages.success(request, "Staff updated successfully!")
        return redirect('admin_panel:staff_list')
    return render(request, 'admin/staff/staff_edit.html', {'staff': staff, 'mode': 'edit'})

@staff_member_required
def staff_delete(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        user = staff.user
        staff.delete()
        user.delete()
        messages.success(request, "Staff deleted successfully!")
        return redirect('admin_panel:staff_list')
    return render(request, 'admin/staff/staff_delete_confirm.html', {'staff': staff})
# END: STAFF_VIEWS

# START: PARENT_VIEWS
@staff_member_required
def parent_list(request):
    query = request.GET.get('search', '')
    parents = Parent.objects.select_related('user', 'linked_student').all()
    if query:
        parents = parents.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(parent_id__icontains=query))
    return render(request, 'admin/parents/parent_list.html', {'parents': parents, 'search': query})

@staff_member_required
def parent_add(request):
    students = Student.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        relationship_type = request.POST.get('relationship_type')
        linked_student_id = request.POST.get('linked_student')
        emergency_contact_number = request.POST.get('emergency_contact_number')

        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already taken.")
            return render(request, 'admin/parents/parent_edit.html', {'mode': 'add', 'students': students})

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        parent_id = f"PAR{user.id:04d}"
        linked_student = Student.objects.filter(id=linked_student_id).first()
        profile_image = request.FILES.get('profile_image')
        Parent.objects.create(user=user, parent_id=parent_id, phone_number=phone_number, address=address, gender=gender, occupation=occupation, relationship_type=relationship_type, linked_student=linked_student, emergency_contact_number=emergency_contact_number, profile_image=profile_image)
        messages.success(request, f"Parent '{first_name} {last_name}' added successfully!")
        return redirect('admin_panel:parent_list')
    return render(request, 'admin/parents/parent_edit.html', {'mode': 'add', 'students': students})

@staff_member_required
def parent_edit(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    students = Student.objects.all()
    if request.method == 'POST':
        parent.user.first_name = request.POST.get('first_name', parent.user.first_name)
        parent.user.last_name = request.POST.get('last_name', parent.user.last_name)
        parent.user.email = request.POST.get('email', parent.user.email)
        parent.user.save()
        parent.phone_number = request.POST.get('phone_number', parent.phone_number)
        parent.address = request.POST.get('address', parent.address)
        parent.gender = request.POST.get('gender', parent.gender)
        parent.occupation = request.POST.get('occupation', parent.occupation)
        parent.relationship_type = request.POST.get('relationship_type', parent.relationship_type)
        parent.emergency_contact_number = request.POST.get('emergency_contact_number', parent.emergency_contact_number)
        linked_student_id = request.POST.get('linked_student')
        parent.linked_student = Student.objects.filter(id=linked_student_id).first()
        if 'profile_image' in request.FILES:
            parent.profile_image = request.FILES['profile_image']
        parent.save()
        messages.success(request, "Parent updated successfully!")
        return redirect('admin_panel:parent_list')
    return render(request, 'admin/parents/parent_edit.html', {'parent': parent, 'mode': 'edit', 'students': students})

@staff_member_required
def parent_delete(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == 'POST':
        user = parent.user
        parent.delete()
        if user:
            user.delete()
        messages.success(request, "Parent deleted successfully!")
        return redirect('admin_panel:parent_list')
    return render(request, 'admin/parents/parent_delete_confirm.html', {'parent': parent})
# END: PARENT_VIEWS

# START: ACCOUNTS_VIEWS
@staff_member_required
def registration_requests(request):
    if request.method == 'POST':
        req_id = request.POST.get('req_id')
        action = request.POST.get('action')
        reg_req = get_object_or_404(RegistrationRequest, id=req_id)
        if action == 'approve':
            if User.objects.filter(email=reg_req.email).exists():
                messages.error(request, f"User with email {reg_req.email} already exists. No new account created.")
            else:
                import string, random
                from django.utils.text import slugify
                from student.models import Student
                from teacher.models import Teacher
                from staff.models import Staff
                from prents.models import Parent as SchoolParent
                
                # 1. Generate Username
                username = slugify(reg_req.first_name + reg_req.last_name)
                if User.objects.filter(username=username).exists():
                    username = f"{username}{random.randint(10, 99)}"
                
                # 2. Generate Random Password
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                # 3. Create User
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=reg_req.email,
                    first_name=reg_req.first_name,
                    last_name=reg_req.last_name
                )
                
                # 4. Create Role Profile
                if reg_req.role == 'Student':
                    Student.objects.create(user=user, phone_number=reg_req.phone_number, student_id=f"STU{random.randint(1000, 9999)}")
                elif reg_req.role == 'Teacher':
                    Teacher.objects.create(user=user, phone_number=reg_req.phone_number, teacher_id=f"TEA{random.randint(1000, 9999)}", salary=0)
                elif reg_req.role == 'Staff':
                    Staff.objects.create(user=user, phone_number=reg_req.phone_number, staff_id=f"STA{random.randint(1000, 9999)}", salary=0)
                elif reg_req.role == 'Parent':
                    SchoolParent.objects.create(user=user, phone_number=reg_req.phone_number, parent_id=f"PAR{random.randint(1000, 9999)}")

                reg_req.is_approved = True
                reg_req.is_rejected = False
                reg_req.save()
                
                # 5. Send Email Notification
                try:
                    from django.core.mail import send_mail
                    from django.conf import settings
                    subject = 'Your School Management System Account'
                    message = f'Hello {reg_req.first_name},\n\nYour registration request has been approved.\n\nUsername: {username}\nPassword: {password}\n\nYou can now login at: http://127.0.0.1:8000/accounts/login/\n\nRegards,\nSchool Admin'
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [reg_req.email], fail_silently=False)
                    reg_req.email_sent = True
                    reg_req.save()
                    messages.success(request, f"Request from '{reg_req.first_name}' approved, user created and email sent successfully!")
                except Exception as e:
                    messages.warning(request, f"User created but failed to send email: {e}")
                
        elif action == 'reject':
            reg_req.is_rejected = True
            reg_req.is_approved = False
            reg_req.save()
            messages.success(request, f"Request from '{reg_req.first_name}' rejected.")
    requests_qs = RegistrationRequest.objects.all().order_by('-created_at')
    return render(request, 'admin/accounts/registration_requests_list.html', {'requests': requests_qs})

@staff_member_required
def user_profiles(request):
    query = request.GET.get('search', '')
    profiles = UserProfile.objects.select_related('user').all()
    if query:
        profiles = profiles.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(user__email__icontains=query))
    return render(request, 'admin/accounts/user_profiles_list.html', {'profiles': profiles, 'search': query})

@staff_member_required
def auth_users(request):
    query = request.GET.get('search', '')
    users = User.objects.all().order_by('-date_joined')
    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query))
    return render(request, 'admin/auth/users_list.html', {'users': users, 'search': query})

@staff_member_required
def auth_groups(request):
    from django.contrib.auth.models import Group
    groups = Group.objects.all()
    return render(request, 'admin/auth/groups_list.html', {'groups': groups})

@staff_member_required
def auth_user_toggle_active(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f"User '{user.username}' has been {status}.")
    return redirect('admin_panel:auth_users')

# START: GALLERY_EDIT_AND_REMEMBER
@staff_member_required
def gallery_edit(request, item_id):
    item = get_object_or_404(Gallery, id=item_id)
    if request.method == 'POST':
        item.title = request.POST.get('title', item.title)
        item.category = request.POST.get('category', item.category)
        if 'file' in request.FILES:
            item.file = request.FILES.get('file')
        item.is_remembered = request.POST.get('is_remembered') == 'on'
        item.reminder_note = request.POST.get('reminder_note', '')
        item.save()
        messages.success(request, f"Gallery item '{item.title}' updated successfully!")
        return redirect('admin_panel:gallery_list')
    return render(request, 'admin/gallery/gallery_form.html', {'item': item})

@staff_member_required
def gallery_toggle_remember(request, item_id):
    item = get_object_or_404(Gallery, id=item_id)
    item.is_remembered = not item.is_remembered
    item.save()
    status = "marked with reminder" if item.is_remembered else "removed from reminders"
    messages.success(request, f"Gallery item '{item.title}' has been {status}!")
    return redirect('admin_panel:gallery_list')
# END: GALLERY_EDIT_AND_REMEMBER

# START: NOTICE_TOGGLE_REMEMBER
@staff_member_required
def notice_toggle_remember(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.is_remembered = not notice.is_remembered
    notice.save()
    status = "marked with reminder" if notice.is_remembered else "removed from reminders"
    messages.success(request, f"Notice '{notice.title}' has been {status}!")
    return redirect('admin_panel:notice_list')
# END: NOTICE_TOGGLE_REMEMBER

# START: REGISTRATION_REQUESTS_CRUD
@staff_member_required
def registration_requests_edit(request, req_id):
    req = get_object_or_404(RegistrationRequest, id=req_id)
    if request.method == 'POST':
        req.first_name = request.POST.get('first_name', req.first_name)
        req.last_name = request.POST.get('last_name', req.last_name)
        req.phone_number = request.POST.get('phone_number', req.phone_number)
        req.role = request.POST.get('role', req.role)
        req.is_remembered = request.POST.get('is_remembered') == 'on'
        req.reminder_note = request.POST.get('reminder_note', '')
        req.save()
        messages.success(request, "Registration request updated!")
        return redirect('admin_panel:registration_requests')
    return render(request, 'admin/accounts/registration_requests_form.html', {'req': req})

@staff_member_required
def registration_requests_delete(request, req_id):
    req = get_object_or_404(RegistrationRequest, id=req_id)
    if request.method == 'POST':
        req.delete()
        messages.success(request, "Registration request deleted!")
        return redirect('admin_panel:registration_requests')
    return render(request, 'admin/accounts/registration_requests_delete_confirm.html', {'req': req})

@staff_member_required
def registration_requests_toggle_remember(request, req_id):
    req = get_object_or_404(RegistrationRequest, id=req_id)
    req.is_remembered = not req.is_remembered
    req.save()
    status = "marked" if req.is_remembered else "unmarked"
    messages.success(request, f"Registration request {status} for reminders.")
    return redirect('admin_panel:registration_requests')
# END: REGISTRATION_REQUESTS_CRUD

# START: USER_PROFILES_CRUD
@staff_member_required
def user_profiles_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        phone = request.POST.get('phone_number')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('admin_panel:user_profiles_add')
            
        user = User.objects.create_user(username=username, email=email, password='defaultpassword')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        UserProfile.objects.create(user=user, role=role, phone_number=phone)
        messages.success(request, "User Profile created successfully!")
        return redirect('admin_panel:user_profiles')
    return render(request, 'admin/accounts/user_profiles_form.html')

@staff_member_required
def user_profiles_edit(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
        profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
        profile.user.email = request.POST.get('email', profile.user.email)
        profile.user.save()
        
        profile.role = request.POST.get('role', profile.role)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.is_remembered = request.POST.get('is_remembered') == 'on'
        profile.reminder_note = request.POST.get('reminder_note', '')
        profile.save()
        messages.success(request, "User Profile updated successfully!")
        return redirect('admin_panel:user_profiles')
    return render(request, 'admin/accounts/user_profiles_form.html', {'profile': profile})

@staff_member_required
def user_profiles_delete(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    if request.method == 'POST':
        user = profile.user
        profile.delete()
        user.delete()
        messages.success(request, "User profile and account deleted!")
        return redirect('admin_panel:user_profiles')
    return render(request, 'admin/accounts/user_profiles_delete_confirm.html', {'profile': profile})

@staff_member_required
def user_profiles_toggle_remember(request, profile_id):
    profile = get_object_or_404(UserProfile, id=profile_id)
    profile.is_remembered = not profile.is_remembered
    profile.save()
    status = "marked" if profile.is_remembered else "unmarked"
    messages.success(request, f"User profile {status} for reminders.")
    return redirect('admin_panel:user_profiles')
# END: USER_PROFILES_CRUD

# START: AUTH_GROUPS_CRUD
@staff_member_required
def auth_groups_add(request):
    from django.contrib.auth.models import Group
    if request.method == 'POST':
        name = request.POST.get('name')
        Group.objects.create(name=name)
        messages.success(request, f"Group '{name}' created!")
        return redirect('admin_panel:auth_groups')
    return render(request, 'admin/auth/groups_form.html')

@staff_member_required
def auth_groups_edit(request, group_id):
    from django.contrib.auth.models import Group
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.name = request.POST.get('name', group.name)
        group.save()
        messages.success(request, "Group updated!")
        return redirect('admin_panel:auth_groups')
    return render(request, 'admin/auth/groups_form.html', {'group': group})

@staff_member_required
def auth_groups_delete(request, group_id):
    from django.contrib.auth.models import Group
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.delete()
        messages.success(request, "Group deleted!")
        return redirect('admin_panel:auth_groups')
    return render(request, 'admin/auth/groups_delete_confirm.html', {'group': group})
# END: AUTH_GROUPS_CRUD

# START: AUTH_USERS_CRUD
@staff_member_required
def auth_users_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('admin_panel:auth_users_add')
        user = User.objects.create_user(username=username, email=email, password='defaultpassword')
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, "User created successfully!")
        return redirect('admin_panel:auth_users')
    return render(request, 'admin/auth/users_form.html')

@staff_member_required
def auth_users_edit(request, user_id):
    edit_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        edit_user.first_name = request.POST.get('first_name', edit_user.first_name)
        edit_user.last_name = request.POST.get('last_name', edit_user.last_name)
        edit_user.email = request.POST.get('email', edit_user.email)
        edit_user.save()
        messages.success(request, "User updated successfully!")
        return redirect('admin_panel:auth_users')
    return render(request, 'admin/auth/users_form.html', {'edit_user': edit_user})

@staff_member_required
def auth_users_delete(request, user_id):
    del_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        del_user.delete()
        messages.success(request, "User deleted!")
        return redirect('admin_panel:auth_users')
    return render(request, 'admin/auth/users_delete_confirm.html', {'del_user': del_user})
# END: AUTH_USERS_CRUD

# END: ACCOUNTS_VIEWS
# END: ADMIN_DASHBOARD_VIEWS

# START: EVENTS_VIEWS
@staff_member_required
def event_list(request):
    from events.models import Event
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'admin/events/event_list.html', {'events': events})

@staff_member_required
def event_add(request):
    from events.models import Event
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        
        Event.objects.create(
            title=title, description=description, date=date,
            time=time, location=location, image=image
        )
        messages.success(request, "Event created successfully!")
        return redirect('admin_panel:event_list')
    return render(request, 'admin/events/event_edit.html')

@staff_member_required
def event_edit(request, event_id):
    from events.models import Event
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.title = request.POST.get('title', event.title)
        event.description = request.POST.get('description', event.description)
        event.date = request.POST.get('date', event.date)
        event.time = request.POST.get('time', event.time)
        event.location = request.POST.get('location', event.location)
        event.is_remembered = request.POST.get('is_remembered') == 'on'
        event.reminder_note = request.POST.get('reminder_note', '')
        
        if 'image' in request.FILES:
            event.image = request.FILES.get('image')
            
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect('admin_panel:event_list')
    return render(request, 'admin/events/event_edit.html', {'event': event})

@staff_member_required
def event_delete(request, event_id):
    from events.models import Event
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        if event.image:
            event.image.delete(save=False)
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('admin_panel:event_list')
    return render(request, 'admin/events/event_delete_confirm.html', {'event': event})

@staff_member_required
def event_toggle_remember(request, event_id):
    from events.models import Event
    event = get_object_or_404(Event, id=event_id)
    event.is_remembered = not event.is_remembered
    if request.method == 'POST':
        reminder_note = request.POST.get('reminder_note', '')
        if reminder_note:
            event.reminder_note = reminder_note
    event.save()
    status = "marked with reminder" if event.is_remembered else "removed from reminders"
    messages.success(request, f"Event '{event.title}' has been {status}!")
    return redirect('admin_panel:event_list')
# END: EVENTS_VIEWS
