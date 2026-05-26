from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from notices.models import Notice
from student.models import Student, Attendance
from teacher.models import Teacher
from academics.models import SchoolClass, Section
import datetime

# START: TEACHER_VIEWS
@login_required
def dashboard(request):
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_teacher=True)).distinct().order_by('-created_at')[:5]
    return render(request, 'teacher/dashboard.html', {'notices': notices})

# --- Attendance Views ---
@login_required
def attendance_mark(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = SchoolClass.objects.all()
    students = []
    sections = []
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    today = datetime.date.today()

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        
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

        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            students = students.filter(section__iexact=selected_section.name.strip())

        if request.method == 'POST':
            date = request.POST.get('date', str(today))
            for student in students:
                status = request.POST.get(f'status_{student.id}', 'Absent')
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={'status': status}
                )
            messages.success(request, f"Attendance for {school_class.name} on {date} has been saved!")
            redirect_url = f"{request.path}?class_id={selected_class}"
            if selected_section_id:
                redirect_url += f"&section_id={selected_section_id}"
            return redirect(redirect_url)

    return render(request, 'teacher/attendance_mark.html', {
        'classes': classes,
        'sections': sections,
        'students': students,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'today': today,
    })

@login_required
def attendance_history(request):
    classes = SchoolClass.objects.all()
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    selected_date = request.GET.get('date', str(datetime.date.today()))
    records = []
    sections = []

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        
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

        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            students = students.filter(section__iexact=selected_section.name.strip())

        for student in students:
            att = Attendance.objects.filter(student=student, date=selected_date).first()
            records.append({
                'student': student,
                'status': att.status if att else 'Not Marked',
            })

    return render(request, 'teacher/attendance_history.html', {
        'classes': classes,
        'sections': sections,
        'records': records,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'selected_date': selected_date,
    })

@login_required
def attendance_absentee(request):
    classes = SchoolClass.objects.all()
    selected_class = request.GET.get('class_id')
    selected_section_id = request.GET.get('section_id')
    selected_date = request.GET.get('date', str(datetime.date.today()))
    absentees = []
    sections = []

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        sections = school_class.sections.all()
        
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
        ).select_related('student')
        
        if selected_section_id:
            selected_section = get_object_or_404(Section, id=selected_section_id)
            absentees_query = absentees_query.filter(student__section__iexact=selected_section.name.strip())
            
        absentees = absentees_query

    return render(request, 'teacher/attendance_absentee.html', {
        'classes': classes,
        'sections': sections,
        'absentees': absentees,
        'selected_class': selected_class,
        'selected_section_id': selected_section_id,
        'selected_date': selected_date,
    })

# --- Marks Entry Views ---
from exams.models import Exam, StudentResult, Grade
from academics.models import Subject

@login_required
def marks_add(request):
    exams = Exam.objects.filter(is_active=True)
    classes = SchoolClass.objects.all()
    selected_exam = request.GET.get('exam_id')
    selected_class = request.GET.get('class_id')
    selected_subject = request.GET.get('subject_id')
    students = []
    subjects = []
    grades = Grade.objects.all()

    if selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        subjects = Subject.objects.filter(school_class=school_class)
        if selected_subject:
            students_qs = Student.objects.filter(current_class=school_class.name)
            subject = get_object_or_404(Subject, id=selected_subject)
            exam = Exam.objects.filter(id=selected_exam).first() if selected_exam else None
            
            students = []
            for s in students_qs:
                existing_result = None
                if exam and subject:
                    existing_result = StudentResult.objects.filter(student=s, exam=exam, subject=subject).first()
                s.existing_marks = existing_result.marks_obtained if existing_result else ""
                students.append(s)

    if request.method == 'POST':
        exam_id = request.POST.get('exam_id')
        subject_id = request.POST.get('subject_id')
        exam = get_object_or_404(Exam, id=exam_id)
        subject = get_object_or_404(Subject, id=subject_id)

        saved_count = 0
        for student in Student.objects.filter(current_class=school_class.name):
            marks_key = f'marks_{student.id}'
            marks_val = request.POST.get(marks_key)
            if marks_val:
                marks = int(marks_val)
                # Auto-assign grade
                grade = Grade.objects.filter(min_mark__lte=marks, max_mark__gte=marks).first()
                StudentResult.objects.update_or_create(
                    student=student, exam=exam, subject=subject,
                    defaults={'marks_obtained': marks, 'grade': grade}
                )
                saved_count += 1
        messages.success(request, f"Marks saved for {saved_count} students successfully!")
        return redirect(f"{request.path}?exam_id={exam_id}&class_id={selected_class}&subject_id={subject_id}")

    return render(request, 'teacher/marks_add.html', {
        'exams': exams, 'classes': classes, 'subjects': subjects,
        'students': students, 'grades': grades,
        'selected_exam': selected_exam, 'selected_class': selected_class, 'selected_subject': selected_subject,
    })

@login_required
def marks_results(request):
    exams = Exam.objects.filter(is_active=True)
    classes = SchoolClass.objects.all()
    selected_exam = request.GET.get('exam_id')
    selected_class = request.GET.get('class_id')
    results = []

    if selected_exam and selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        results = StudentResult.objects.filter(
            exam_id=selected_exam,
            student__current_class=school_class.name
        ).select_related('student', 'subject', 'grade', 'exam').order_by('subject__name', 'student__roll_number')

    return render(request, 'teacher/marks_results.html', {
        'exams': exams, 'classes': classes,
        'results': results,
        'selected_exam': selected_exam, 'selected_class': selected_class,
    })

@login_required
def marks_report(request):
    exams = Exam.objects.filter(is_active=True)
    classes = SchoolClass.objects.all()
    selected_exam = request.GET.get('exam_id')
    selected_class = request.GET.get('class_id')
    report_data = []

    if selected_exam and selected_class:
        school_class = get_object_or_404(SchoolClass, id=selected_class)
        students = Student.objects.filter(current_class=school_class.name)
        for student in students:
            results = StudentResult.objects.filter(exam_id=selected_exam, student=student).select_related('subject', 'grade')
            total = sum(r.marks_obtained for r in results)
            count = results.count()
            avg = total / count if count else 0
            report_data.append({'student': student, 'results': results, 'total': total, 'average': avg})

    return render(request, 'teacher/marks_report.html', {
        'exams': exams, 'classes': classes,
        'report_data': report_data,
        'selected_exam': selected_exam, 'selected_class': selected_class,
    })
# END: TEACHER_VIEWS
