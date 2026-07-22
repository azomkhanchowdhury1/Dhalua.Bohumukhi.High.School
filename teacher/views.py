from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from notices.models import Notice
from student.models import Student, Attendance, ClassAttendance, StudentHomework
from teacher.models import Teacher, SalaryPayment, TeacherHomework
from academics.models import SchoolClass, Section, Subject
import datetime

# START: TEACHER_VIEWS
@login_required
def dashboard(request):
    # TEMPORARY AUTO MIGRATION
    from django.core.management import call_command
    try:
        call_command('makemigrations', 'teacher')
        call_command('migrate', 'teacher')
        call_command('makemigrations', 'exams')
        call_command('migrate', 'exams')
    except Exception as e:
        print("Auto-migration failed:", e)

    notices = Notice.objects.filter(Q(is_public=True) | Q(target_teacher=True)).distinct().order_by('-created_at')[:5]
    today = datetime.date.today()


    # Real stat data
    teacher = Teacher.objects.filter(user=request.user).first()

    # Classes Today: distinct classes held today by this teacher
    classes_today = ClassAttendance.objects.filter(teacher=teacher, date=today).count() if teacher else 0
    next_class = ClassAttendance.objects.filter(teacher=teacher, date=today, time__gt=datetime.datetime.now().time()).order_by('time').first() if teacher else None

    # Total Students: students in classes this teacher teaches
    total_students = Student.objects.count()

    # Pending Submissions: StudentHomework items without a grade/review for this teacher
    pending_submissions = StudentHomework.objects.filter(teacher=teacher, graded=False).count() if teacher else 0

    # Leave Balance: approved leaves this month (count used)
    leave_used = SalaryPayment.objects.filter(teacher=teacher).count() if teacher else 0  # placeholder until leave model exists
    leave_balance = max(0, 10 - leave_used)  # assume 10 days annual leave

    return render(request, 'teacher/dashboard.html', {
        'notices': notices,
        'classes_today': classes_today,
        'next_class': next_class,
        'total_students': total_students,
        'pending_submissions': pending_submissions,
        'leave_balance': leave_balance,
    })

# --- Stat Detail Views ---
@login_required
def stat_classes_today(request):
    """Shows all classes held today by this teacher."""
    teacher = Teacher.objects.filter(user=request.user).first()
    today = datetime.date.today()
    classes = ClassAttendance.objects.filter(
        teacher=teacher, date=today
    ).select_related('school_class', 'section', 'subject').order_by('time') if teacher else []

    present_counts = {}
    absent_counts = {}
    for cls in classes:
        present_counts[cls.id] = cls.student_attendances.filter(status='Present').count()
        absent_counts[cls.id] = cls.student_attendances.filter(status='Absent').count()

    return render(request, 'teacher/stat_classes_today.html', {
        'classes': classes,
        'today': today,
        'present_counts': present_counts,
        'absent_counts': absent_counts,
    })

@login_required
def stat_total_students(request):
    """Shows all students with class & section breakdown."""
    students = Student.objects.all().order_by('current_class', 'section', 'roll_number')
    class_groups = {}
    for s in students:
        key = s.current_class or 'Unassigned'
        class_groups.setdefault(key, []).append(s)
    total = students.count()
    return render(request, 'teacher/stat_total_students.html', {
        'students': students,
        'class_groups': class_groups,
        'total': total,
    })

@login_required
def stat_pending_submissions(request):
    """Shows pending homework/assignment submissions."""
    teacher = Teacher.objects.filter(user=request.user).first()
    submissions = StudentHomework.objects.filter(teacher=teacher, graded=False).select_related('student').order_by('-submitted_at') if teacher else StudentHomework.objects.none()
    return render(request, 'teacher/stat_pending_submissions.html', {
        'submissions': submissions,
        'count': submissions.count(),
    })

@login_required
def stat_leave_balance(request):
    """Shows leave balance and history."""
    teacher = Teacher.objects.filter(user=request.user).first()
    salary_payments = SalaryPayment.objects.filter(teacher=teacher).order_by('-payment_date') if teacher else []
    leave_used = salary_payments.count()
    leave_balance = max(0, 10 - leave_used)
    return render(request, 'teacher/stat_leave_balance.html', {
        'teacher': teacher,
        'salary_payments': salary_payments,
        'leave_balance': leave_balance,
        'leave_used': leave_used,
        'leave_total': 10,
    })

# --- Attendance Views ---

@login_required
def attendance_mark(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = SchoolClass.objects.all()
    students = []
    sections = []
    subjects = []
    
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    selected_subject_id = request.GET.get('subject_id')
    today = datetime.date.today()

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        subjects = school_class.subjects.all()
        
        # Build robust class matching queries
        class_name_clean = school_class.name.strip()
        alternatives = [class_name_clean]
        mapping = {
            'SIX': ['6', 'Class 6', 'Class Six', 'Six'],
            'SEVEN': ['7', 'Class 7', 'Class Seven', 'Seven'],
            'EIGHT': ['8', 'Class 8', 'Class Eight', 'Eight'],
            'NINE': ['9', 'Class 9', 'Class Nine', 'Nine'],
            'TEN': ['10', 'Class 10', 'Class Ten', 'Ten'],
            '6': ['SIX', 'Class 6', 'Class Six', 'Six'],
            '7': ['SEVEN', 'Class 7', 'Class Seven', 'Seven'],
            '8': ['EIGHT', 'Class 8', 'Class Eight', 'Eight'],
            '9': ['NINE', 'Class 9', 'Class Nine', 'Nine'],
            '10': ['TEN', 'Class 10', 'Class Ten', 'Ten']
        }
        for key, vals in mapping.items():
            if class_name_clean.upper() == key:
                alternatives.extend(vals)
                break
        
        query = Q()
        for alt in alternatives:
            query |= Q(current_class__iexact=alt) | Q(current_class__iexact=alt.strip())
            
        students = Student.objects.filter(query)

        selected_section = None
        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            students = students.filter(section__iexact=selected_section.name.strip())

        if request.method == 'POST':
            date = request.POST.get('date', str(today))
            time = request.POST.get('time')
            subject_id = request.POST.get('subject_id')
            
            if not subject_id:
                messages.error(request, "Please select a subject.")
                return redirect(f"{request.path}?class_id={selected_class}&section_id={selected_section_id or ''}")
            
            subject = get_object_or_404(Subject, id=subject_id)
            
            class_att, created = ClassAttendance.objects.update_or_create(
                teacher=teacher,
                school_class=school_class,
                section=selected_section,
                subject=subject,
                date=date,
                defaults={'time': time, 'is_held': True}
            )

            for student in students:
                status = request.POST.get(f'status_{student.id}', 'Absent')
                Attendance.objects.update_or_create(
                    class_attendance=class_att,
                    student=student,
                    defaults={'date': date, 'status': status}
                )
            messages.success(request, f"Attendance for {school_class.name} on {date} has been saved!")
            
            redirect_url = f"{request.path}?class_id={selected_class}"
            if selected_section_id:
                redirect_url += f"&section_id={selected_section_id}"
            if subject_id:
                redirect_url += f"&subject_id={subject_id}"
            return redirect(redirect_url)

    return render(request, 'teacher/attendance_mark.html', {
        'classes': classes,
        'sections': sections,
        'subjects': subjects,
        'students': students,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'selected_subject_id': selected_subject_id,
        'today': today,
    })

@login_required
def attendance_history(request):
    classes = SchoolClass.objects.all()
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    selected_subject_id = request.GET.get('subject_id')
    selected_date = request.GET.get('date', str(datetime.date.today()))
    
    records = []
    sections = []
    subjects = []
    class_att = None
    is_held = True

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        subjects = school_class.subjects.all()
        
        # Build robust class matching queries
        class_name_clean = school_class.name.strip()
        alternatives = [class_name_clean]
        mapping = {
            'SIX': ['6', 'Class 6', 'Class Six', 'Six'],
            'SEVEN': ['7', 'Class 7', 'Class Seven', 'Seven'],
            'EIGHT': ['8', 'Class 8', 'Class Eight', 'Eight'],
            'NINE': ['9', 'Class 9', 'Class Nine', 'Nine'],
            'TEN': ['10', 'Class 10', 'Class Ten', 'Ten'],
            '6': ['SIX', 'Class 6', 'Class Six', 'Six'],
            '7': ['SEVEN', 'Class 7', 'Class Seven', 'Seven'],
            '8': ['EIGHT', 'Class 8', 'Class Eight', 'Eight'],
            '9': ['NINE', 'Class 9', 'Class Nine', 'Nine'],
            '10': ['TEN', 'Class 10', 'Class Ten', 'Ten']
        }
        for key, vals in mapping.items():
            if class_name_clean.upper() == key:
                alternatives.extend(vals)
                break
        
        query = Q()
        for alt in alternatives:
            query |= Q(current_class__iexact=alt) | Q(current_class__iexact=alt.strip())
            
        students = Student.objects.filter(query)

        selected_section = None
        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            students = students.filter(section__iexact=selected_section.name.strip())

        if selected_subject_id:
            class_att = ClassAttendance.objects.filter(
                school_class=school_class,
                section=selected_section,
                subject_id=selected_subject_id,
                date=selected_date
            ).first()
            
            if class_att:
                is_held = class_att.is_held
                for student in students:
                    att = Attendance.objects.filter(student=student, class_attendance=class_att).first()
                    records.append({
                        'student': student,
                        'status': att.status if att else 'Not Marked',
                    })
            else:
                is_held = False # No class attendance record found

        if request.method == 'POST':
            if class_att:
                is_held_post = request.POST.get('is_held') == 'on'
                class_att.is_held = is_held_post
                class_att.save()
                
                if is_held_post:
                    for student in students:
                        status = request.POST.get(f'status_{student.id}')
                        if status:
                            Attendance.objects.update_or_create(
                                class_attendance=class_att,
                                student=student,
                                defaults={'date': selected_date, 'status': status}
                            )
                
                messages.success(request, "Attendance history updated.")
            
            redirect_url = f"{request.path}?class_id={selected_class}&date={selected_date}"
            if selected_section_id:
                redirect_url += f"&section_id={selected_section_id}"
            if selected_subject_id:
                redirect_url += f"&subject_id={selected_subject_id}"
            return redirect(redirect_url)

    return render(request, 'teacher/attendance_history.html', {
        'classes': classes,
        'sections': sections,
        'subjects': subjects,
        'records': records,
        'class_att': class_att,
        'is_held': is_held,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'selected_subject_id': selected_subject_id,
        'selected_date': selected_date,
    })

@login_required
def attendance_absentee(request):
    classes = SchoolClass.objects.all()
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    selected_subject_id = request.GET.get('subject_id')
    selected_date = request.GET.get('date', str(datetime.date.today()))
    absentees = []
    sections = []
    subjects = []

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        subjects = school_class.subjects.all()
        
        # Build robust class matching queries
        class_name_clean = school_class.name.strip()
        alternatives = [class_name_clean]
        mapping = {
            'SIX': ['6', 'Class 6', 'Class Six', 'Six'],
            'SEVEN': ['7', 'Class 7', 'Class Seven', 'Seven'],
            'EIGHT': ['8', 'Class 8', 'Class Eight', 'Eight'],
            'NINE': ['9', 'Class 9', 'Class Nine', 'Nine'],
            'TEN': ['10', 'Class 10', 'Class Ten', 'Ten'],
            '6': ['SIX', 'Class 6', 'Class Six', 'Six'],
            '7': ['SEVEN', 'Class 7', 'Class Seven', 'Seven'],
            '8': ['EIGHT', 'Class 8', 'Class Eight', 'Eight'],
            '9': ['NINE', 'Class 9', 'Class Nine', 'Nine'],
            '10': ['TEN', 'Class 10', 'Class Ten', 'Ten']
        }
        for key, vals in mapping.items():
            if class_name_clean.upper() == key:
                alternatives.extend(vals)
                break
        
        query = Q()
        for alt in alternatives:
            query |= Q(student__current_class__iexact=alt) | Q(student__current_class__iexact=alt.strip())

        absentees_query = Attendance.objects.filter(
            query,
            date=selected_date,
            status='Absent'
        ).select_related('student', 'class_attendance')
        
        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            absentees_query = absentees_query.filter(student__section__iexact=selected_section.name.strip())
            
        if selected_subject_id:
            absentees_query = absentees_query.filter(class_attendance__subject_id=selected_subject_id)
            
        absentees = absentees_query

    return render(request, 'teacher/attendance_absentee.html', {
        'classes': classes,
        'sections': sections,
        'subjects': subjects,
        'absentees': absentees,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'selected_subject_id': selected_subject_id,
        'selected_date': selected_date,
    })

# --- Marks Entry Views ---
from exams.models import Exam, StudentResult, Grade, ExamSchedule
from academics.models import Subject

def _get_students_for_class(school_class):
    class_name_clean = school_class.name.strip()
    alternatives = [class_name_clean]
    mapping = {
        'SIX': ['6', 'Class 6', 'Class Six', 'Six'],
        'SEVEN': ['7', 'Class 7', 'Class Seven', 'Seven'],
        'EIGHT': ['8', 'Class 8', 'Class Eight', 'Eight'],
        'NINE': ['9', 'Class 9', 'Class Nine', 'Nine'],
        'TEN': ['10', 'Class 10', 'Class Ten', 'Ten'],
        '6': ['SIX', 'Class 6', 'Class Six', 'Six'],
        '7': ['SEVEN', 'Class 7', 'Class Seven', 'Seven'],
        '8': ['EIGHT', 'Class 8', 'Class Eight', 'Eight'],
        '9': ['NINE', 'Class 9', 'Class Nine', 'Nine'],
        '10': ['TEN', 'Class 10', 'Class Ten', 'Ten']
    }
    for key, vals in mapping.items():
        if class_name_clean.upper() == key:
            alternatives.extend(vals)
            break
    
    query = Q()
    for alt in alternatives:
        query |= Q(current_class__iexact=alt) | Q(current_class__iexact=alt.strip())
        
    return Student.objects.filter(query)

@login_required
def marks_add(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    active_tab = request.GET.get('tab', 'add_marks')  # class_tests | add_marks | results | report

    # ============ COMMON DATA ============
    all_class_tests = Exam.objects.filter(
        exam_type='Class Test', created_by_teacher=teacher
    ).prefetch_related('examschedule_set').order_by('-id')
    for test in all_class_tests:
        test.schedule = test.examschedule_set.first()

    classes = SchoolClass.objects.all()
    sections = Section.objects.all()
    all_subjects = Subject.objects.all()
    grades = Grade.objects.all()

    # Published exams for marks entry dropdown
    exams = Exam.objects.filter(is_active=True, exam_type='Class Test', created_by_teacher=teacher)

    # ============ TAB 1: CLASS TEST CREATION (POST) ============
    if request.method == 'POST':
        action = request.POST.get('action', '')

        # --- Create new class test ---
        if action == 'create_class_test':
            title = request.POST.get('title')
            class_id = request.POST.get('class_id')
            section_id = request.POST.get('section_id')
            subject_id = request.POST.get('subject_id')
            exam_date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            total_marks = request.POST.get('total_marks', 100)
            instructions = request.POST.get('instructions', '')
            publish = 'publish_btn' in request.POST

            s_class = get_object_or_404(SchoolClass, id=class_id)
            subject = get_object_or_404(Subject, id=subject_id)
            section = get_object_or_404(Section, id=section_id) if section_id else None

            current_year = str(datetime.date.today().year)
            exam = Exam.objects.create(
                name=title,
                year=current_year,
                exam_type='Class Test',
                created_by_teacher=teacher,
                is_published=publish,
                is_active=True
            )
            ExamSchedule.objects.create(
                exam=exam,
                school_class=s_class,
                section=section,
                subject=subject,
                date=exam_date,
                start_time=start_time,
                end_time=end_time or None,
                total_marks=total_marks,
                instructions=instructions
            )
            messages.success(request, f"Class Test '{title}' created successfully!")
            return redirect(f"{request.path}?tab=class_tests")

        # --- Edit existing class test ---
        elif action == 'edit_class_test':
            test_id = request.POST.get('test_id')
            exam = get_object_or_404(Exam, id=test_id, created_by_teacher=teacher, exam_type='Class Test')
            schedule = exam.examschedule_set.first()

            title = request.POST.get('title')
            class_id = request.POST.get('class_id')
            section_id = request.POST.get('section_id')
            subject_id = request.POST.get('subject_id')
            exam_date = request.POST.get('date')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            total_marks = request.POST.get('total_marks', 100)
            instructions = request.POST.get('instructions', '')
            publish = 'publish_btn' in request.POST

            s_class = get_object_or_404(SchoolClass, id=class_id)
            subject = get_object_or_404(Subject, id=subject_id)
            section = get_object_or_404(Section, id=section_id) if section_id else None

            exam.name = title
            exam.is_published = publish
            exam.save()

            if schedule:
                schedule.school_class = s_class
                schedule.section = section
                schedule.subject = subject
                schedule.date = exam_date
                schedule.start_time = start_time
                schedule.end_time = end_time or None
                schedule.total_marks = total_marks
                schedule.instructions = instructions
                schedule.save()
            else:
                ExamSchedule.objects.create(
                    exam=exam, school_class=s_class, section=section, subject=subject,
                    date=exam_date, start_time=start_time, end_time=end_time or None,
                    total_marks=total_marks, instructions=instructions
                )
            messages.success(request, f"Class Test '{title}' updated successfully!")
            return redirect(f"{request.path}?tab=class_tests")

        # --- Delete class test ---
        elif action == 'delete_class_test':
            test_id = request.POST.get('test_id')
            exam = get_object_or_404(Exam, id=test_id, created_by_teacher=teacher, exam_type='Class Test')
            name = exam.name
            exam.delete()
            messages.success(request, f"Class Test '{name}' deleted successfully!")
            return redirect(f"{request.path}?tab=class_tests")

        # --- Toggle publish ---
        elif action == 'toggle_publish':
            test_id = request.POST.get('test_id')
            exam = get_object_or_404(Exam, id=test_id, created_by_teacher=teacher, exam_type='Class Test')
            exam.is_published = not exam.is_published
            exam.save()
            status = 'published' if exam.is_published else 'unpublished'
            messages.success(request, f"Class Test '{exam.name}' is now {status}!")
            return redirect(f"{request.path}?tab=class_tests")

        # --- Save marks ---
        elif action == 'save_marks':
            exam_id = request.POST.get('exam_id')
            subject_id = request.POST.get('subject_id')
            class_id = request.POST.get('class_id')
            exam = get_object_or_404(Exam, id=exam_id, created_by_teacher=teacher)
            subject = get_object_or_404(Subject, id=subject_id)
            schedule = exam.examschedule_set.first()

            school_class = get_object_or_404(SchoolClass, id=class_id)
            students_qs = _get_students_for_class(school_class)
            if schedule and schedule.section:
                students_qs = students_qs.filter(section=schedule.section.name)

            saved_count = 0
            for student in students_qs:
                marks_key = f'marks_{student.id}'
                marks_val = request.POST.get(marks_key)
                if marks_val:
                    marks = float(marks_val)
                    norm_marks = marks
                    if schedule and schedule.total_marks > 0:
                        norm_marks = (marks / schedule.total_marks) * 100
                    grade = Grade.objects.filter(min_mark__lte=norm_marks, max_mark__gte=norm_marks).first()
                    StudentResult.objects.update_or_create(
                        student=student, exam=exam, subject=subject,
                        defaults={'marks_obtained': marks, 'grade': grade}
                    )
                    saved_count += 1
            messages.success(request, f"{saved_count} জন শিক্ষার্থীর marks সফলভাবে সংরক্ষিত হয়েছে!")
            return redirect(f"{request.path}?tab=add_marks&exam_id={exam_id}&class_id={class_id}&subject_id={subject_id}")

    # ============ TAB 2: ADD MARKS — filter data ============
    selected_exam = request.GET.get('exam_id')
    selected_class = request.GET.get('class_id')
    selected_subject = request.GET.get('subject_id')
    selected_exam = int(selected_exam) if selected_exam else None
    selected_class = int(selected_class) if selected_class else None
    selected_subject = int(selected_subject) if selected_subject else None
    students = []
    subjects = []
    total_marks = 100

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        subjects = Subject.objects.filter(school_class=school_class)

        if selected_subject and selected_exam:
            subject = get_object_or_404(Subject, id=selected_subject)
            exam = Exam.objects.filter(id=selected_exam, created_by_teacher=teacher).first()
            schedule = exam.examschedule_set.first() if exam else None

            students_qs = _get_students_for_class(school_class)
            if schedule and schedule.section:
                students_qs = students_qs.filter(section=schedule.section.name)
            if schedule:
                total_marks = schedule.total_marks

            for s in students_qs:
                existing_result = StudentResult.objects.filter(student=s, exam=exam, subject=subject).first() if exam else None
                s.existing_marks = existing_result.marks_obtained if existing_result else ''
                students.append(s)

    # ============ TAB 3: VIEW RESULTS ============
    res_exam_id = request.GET.get('res_exam_id')
    res_class_id = request.GET.get('res_class_id')
    res_exam_id = int(res_exam_id) if res_exam_id else None
    res_class_id = int(res_class_id) if res_class_id else None
    results = []
    if res_exam_id and res_class_id:
        res_class = get_object_or_404(SchoolClass, id=res_class_id)
        students_qs = _get_students_for_class(res_class)
        results = StudentResult.objects.filter(
            exam_id=res_exam_id,
            exam__created_by_teacher=teacher,
            student__in=students_qs
        ).select_related('student', 'subject', 'grade', 'exam').order_by('subject__name', 'student__roll_number')

    # ============ TAB 4: PROGRESS REPORT ============
    rpt_exam_id = request.GET.get('rpt_exam_id')
    rpt_class_id = request.GET.get('rpt_class_id')
    rpt_exam_id = int(rpt_exam_id) if rpt_exam_id else None
    rpt_class_id = int(rpt_class_id) if rpt_class_id else None
    rpt_students = []
    report_data = []
    if rpt_exam_id and rpt_class_id:
        rpt_class = get_object_or_404(SchoolClass, id=rpt_class_id)
        rpt_students = _get_students_for_class(rpt_class)
        for student in rpt_students:
            stu_results = StudentResult.objects.filter(
                exam_id=rpt_exam_id, exam__created_by_teacher=teacher, student=student
            ).select_related('subject', 'grade')
            total = sum(r.marks_obtained for r in stu_results)
            count = stu_results.count()
            avg = total / count if count else 0
            report_data.append({'student': student, 'results': stu_results, 'total': total, 'average': avg})

    # Convert querysets to lists to store the annotated selection states securely
    exams = list(exams)
    classes = list(classes)
    subjects = list(subjects)

    for exam in exams:
        exam.is_selected = (exam.id == selected_exam)
        exam.res_selected = (exam.id == res_exam_id)
        exam.rpt_selected = (exam.id == rpt_exam_id)

    for cls in classes:
        cls.is_selected = (cls.id == selected_class)
        cls.res_selected = (cls.id == res_class_id)
        cls.rpt_selected = (cls.id == rpt_class_id)

    for sub in subjects:
        sub.is_selected = (sub.id == selected_subject)

    return render(request, 'teacher/marks_add.html', {
        # Tab state
        'active_tab': active_tab,
        # Tab 1 — class tests
        'tests': all_class_tests,
        'sections': sections,
        'all_subjects': all_subjects,
        # Tab 2 — add marks
        'exams': exams,
        'classes': classes,
        'subjects': subjects,
        'students': students,
        'grades': grades,
        'selected_exam': selected_exam,
        'selected_class': selected_class,
        'selected_subject': selected_subject,
        'total_marks': total_marks,
        # Tab 3 — results
        'results': results,
        'res_exam_id': res_exam_id,
        'res_class_id': res_class_id,
        # Tab 4 — report
        'report_data': report_data,
        'rpt_exam_id': rpt_exam_id,
        'rpt_class_id': rpt_class_id,
    })

@login_required
def marks_results(request):
    # All results functionality is now in marks_add (tab=results)
    return redirect('/teacher/marks/add/?tab=results')

@login_required
def marks_report(request):
    # All report functionality is now in marks_add (tab=report)
    return redirect('/teacher/marks/add/?tab=report')

# --- Class Test CRUD Views (now all handled inside marks_add) ---
@login_required
def class_test_list(request):
    return redirect('/teacher/marks/add/?tab=class_tests')

@login_required
def class_test_edit(request, test_id):
    return redirect('/teacher/marks/add/?tab=class_tests')

@login_required
def class_test_delete(request, test_id):
    return redirect('/teacher/marks/add/?tab=class_tests')

@login_required
def class_test_toggle_publish(request, test_id):
    teacher = get_object_or_404(Teacher, user=request.user)
    exam = get_object_or_404(Exam, id=test_id, created_by_teacher=teacher, exam_type='Class Test')
    exam.is_published = not exam.is_published
    exam.save()
    status = 'published' if exam.is_published else 'unpublished'
    messages.success(request, f"Class Test '{exam.name}' is now {status}!")
    return redirect('/teacher/marks/add/?tab=class_tests')

# --- My Schedule Views ---
@login_required
def today_routine(request):
    return render(request, 'teacher/today_routine.html')

@login_required
def weekly_timetable(request):
    return render(request, 'teacher/weekly_timetable.html')

@login_required
def proxy_classes(request):
    return render(request, 'teacher/proxy_classes.html')

# --- Assignments Views ---
@login_required
def create_assignment(request):
    return render(request, 'teacher/create_assignment.html')

@login_required
def review_submissions(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    submissions = StudentHomework.objects.filter(teacher=teacher).select_related('student__user').order_by('-submitted_at') if teacher else StudentHomework.objects.none()

    if request.method == 'POST':
        hw_id = request.POST.get('homework_id')
        marks_val = request.POST.get('marks', '').strip()
        feedback_val = request.POST.get('feedback', '').strip()
        hw = get_object_or_404(StudentHomework, id=hw_id, teacher=teacher)
        if marks_val:
            hw.marks = marks_val
            hw.graded = True
        if feedback_val:
            hw.feedback = feedback_val
        hw.save()
        messages.success(request, f"Graded homework '{hw.title}' successfully!")
        return redirect('teacher:review_submissions')

    return render(request, 'teacher/review_submissions.html', {
        'submissions': submissions,
    })

@login_required
def study_material(request):
    return render(request, 'teacher/study_material.html')

# --- Payroll & HR Views ---
@login_required
def salary_slips(request):
    from finance.models import PayoutRequest
    teacher = Teacher.objects.filter(user=request.user).first()
    salaries = SalaryPayment.objects.filter(teacher=teacher).order_by('-payment_date') if teacher else []
    payout_requests = PayoutRequest.objects.filter(user=request.user).order_by('-requested_at')

    if request.method == 'POST':
        amount = request.POST.get('amount', '').strip()
        method = request.POST.get('payment_method', '').strip()
        account = request.POST.get('account_details', '').strip()
        if amount and method and account:
            PayoutRequest.objects.create(
                user=request.user,
                amount=amount,
                payment_method=method,
                account_details=account
            )
            messages.success(request, 'পেআউট রিকোয়েস্ট সাবমিট হয়েছে! অ্যাডমিন অনুমোদন করলে টাকা পাঠানো হবে।')
        else:
            messages.error(request, 'সব তথ্য পূরণ করুন।')
        return redirect('teacher:salary_slips')

    return render(request, 'teacher/salary_slips.html', {
        'salaries': salaries,
        'payout_requests': payout_requests,
        'teacher': teacher,
    })

@login_required
def leave_request(request):
    return render(request, 'teacher/leave_request.html')

@login_required
def my_profile(request):
    return render(request, 'teacher/my_profile.html')

# --- Online Classes ---
from academics.models import OnlineClass
import datetime

@login_required
def online_classes(request):
    teacher = Teacher.objects.filter(user=request.user).first()
    
    # Categorize classes
    now = datetime.datetime.now()
    live_classes = OnlineClass.objects.filter(teacher=teacher, status='Live').order_by('start_time') if teacher else []
    scheduled_classes = OnlineClass.objects.filter(teacher=teacher, status='Scheduled').order_by('start_time') if teacher else []
    recorded_classes = OnlineClass.objects.filter(teacher=teacher, status='Recorded').order_by('-start_time') if teacher else []
    
    return render(request, 'online_classes.html', {
        'live_classes': live_classes,
        'scheduled_classes': scheduled_classes,
        'recorded_classes': recorded_classes,
        'is_teacher': True
    })

@login_required
def student_messages(request):
    # Get all students to list in sidebar
    students = Student.objects.select_related('user').all().order_by('user__first_name')
    return render(request, 'teacher/student_messages.html', {'students': students})

@login_required
def chat_student(request):
    from django.http import JsonResponse
    from staff.models import DirectMessage
    student_id = request.GET.get('student_id') or request.POST.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    student_user = student.user

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
                receiver=student_user,
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
        Q(sender=request.user, receiver=student_user) |
        Q(sender=student_user, receiver=request.user)
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
    DirectMessage.objects.filter(sender=student_user, receiver=request.user, is_read=False).update(is_read=True)

    return JsonResponse({
        'status': 'success',
        'messages': msg_list,
        'current_user_id': request.user.id
    })

# START: HOMEWORK_UPLOAD_VIEWS
@login_required
def upload_homework(request):
    """Teacher can upload homework for students."""
    teacher = Teacher.objects.filter(user=request.user).first()
    classes = SchoolClass.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subject = request.POST.get('subject', '').strip()
        school_class = request.POST.get('school_class', '').strip()
        section = request.POST.get('section', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date') or None
        file = request.FILES.get('file')

        if title and subject and school_class:
            TeacherHomework.objects.create(
                teacher=teacher,
                title=title,
                subject=subject,
                school_class=school_class,
                section=section,
                description=description,
                due_date=due_date,
                file=file,
            )
            messages.success(request, f"Homework '{title}' uploaded successfully!")
            return redirect('teacher:upload_homework')
        else:
            messages.error(request, "Please fill in all required fields.")

    homeworks = TeacherHomework.objects.filter(teacher=teacher).order_by('-uploaded_at') if teacher else TeacherHomework.objects.none()
    return render(request, 'teacher/upload_homework.html', {
        'homeworks': homeworks,
        'classes': classes,
        'subjects': subjects,
    })


@login_required
def delete_homework(request, hw_id):
    """Delete a teacher-uploaded homework entry."""
    teacher = Teacher.objects.filter(user=request.user).first()
    hw = get_object_or_404(TeacherHomework, id=hw_id, teacher=teacher)
    hw.delete()
    messages.success(request, "Homework deleted successfully.")
    return redirect('teacher:upload_homework')
# END: HOMEWORK_UPLOAD_VIEWS

# END: TEACHER_VIEWS
