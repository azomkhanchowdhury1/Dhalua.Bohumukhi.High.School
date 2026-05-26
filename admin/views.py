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
    students = Student.objects.all()
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status}
                )
        messages.success(request, "Attendance updated successfully!")
    return render(request, 'admin/students/attendance.html', {'students': students})

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
# END: ADMIN_DASHBOARD_VIEWS
