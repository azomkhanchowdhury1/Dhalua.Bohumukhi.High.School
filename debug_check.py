import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from academics.models import SchoolClass, Timetable, Syllabus
from teacher.models import Teacher
from student.models import Student, ClassAttendance
from django.db.models import Q

current_class = '8'

print("=== _get_school_class debug ===")
# Step 1
cls = SchoolClass.objects.filter(name=current_class).first()
print(f"Step 1 exact match for '{current_class}': {cls}")

# Step 2
cls = SchoolClass.objects.filter(name__icontains=current_class).first()
print(f"Step 2 icontains name for '{current_class}': {cls}")

# Step 3
stripped = current_class.replace('Class ', '').replace('class ', '').strip()
print(f"Stripped value: '{stripped}'")
cls = SchoolClass.objects.filter(
    Q(name__icontains=stripped) | Q(code__icontains=stripped)
).first()
print(f"Step 3 result: {cls}")

print("\n=== All SchoolClasses raw ===")
for c in SchoolClass.objects.all():
    name = c.name
    code = c.code
    print(f"  Name='{name}' | Code='{code}' | '8' in name={repr('8' in name)} | '8' in code={repr('8' in code)}")

print("\n=== Final school_class_obj ===")
# Simulate the full function
def _get_school_class(current_class_str):
    if not current_class_str:
        return None
    cls = SchoolClass.objects.filter(name=current_class_str).first()
    if cls:
        return cls
    cls = SchoolClass.objects.filter(name__icontains=current_class_str).first()
    if cls:
        return cls
    stripped = current_class_str.replace('Class ', '').replace('class ', '').strip()
    cls = SchoolClass.objects.filter(
        Q(name__icontains=stripped) | Q(code__icontains=stripped)
    ).first()
    return cls

school_class_obj = _get_school_class('8')
print(f"school_class_obj = {school_class_obj}")

if school_class_obj:
    timetable = Timetable.objects.filter(section__school_class=school_class_obj).order_by('day', 'start_time')
    print(f"\n=== Timetable entries ({timetable.count()}) ===")
    for t in timetable:
        print(f"  {t}")

    syllabus = Syllabus.objects.filter(subject__school_class=school_class_obj).order_by('-uploaded_at')
    print(f"\n=== Syllabus entries ({syllabus.count()}) ===")
    for s in syllabus:
        print(f"  {s}")

    teacher_ids = ClassAttendance.objects.filter(school_class=school_class_obj).values_list('teacher_id', flat=True).distinct()
    teachers = Teacher.objects.filter(id__in=teacher_ids)
    print(f"\n=== Teachers via ClassAttendance ({teachers.count()}) ===")
    if not teachers.exists():
        teachers = Teacher.objects.all()
        print("  (fallback: all teachers)")
    for t in teachers:
        print(f"  {t}")
else:
    print("school_class_obj is None — queries return empty!")
    print("Timetable: EMPTY")
    print("Syllabus: EMPTY")
    print("Teachers (fallback): all")
    for t in Teacher.objects.all():
        print(f"  {t}")
