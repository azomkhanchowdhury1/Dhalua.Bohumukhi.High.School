import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from academics.models import SchoolClass

print("=== Cleaning SchoolClass names (trim whitespace) ===")
for c in SchoolClass.objects.all():
    old_name = c.name
    new_name = c.name.strip()
    if old_name != new_name:
        c.name = new_name
        c.save()
        print(f"  Fixed: '{old_name}' -> '{new_name}'")
    else:
        print(f"  OK: '{c.name}' (no change)")

print("\n=== Final SchoolClass list ===")
for c in SchoolClass.objects.all():
    print(f"  ID:{c.id} Name:{c.name!r} Code:{c.code!r}")

# Verify student current_class matches
from student.models import Student
print("\n=== Student current_class verification ===")
for s in Student.objects.all():
    matched = SchoolClass.objects.filter(name=s.current_class).first()
    print(f"  Student: {s} | current_class: {s.current_class!r} | Exact match: {matched}")

print("\n=== All data counts ===")
from academics.models import Timetable, Syllabus, Subject
from teacher.models import Teacher

school_class = SchoolClass.objects.filter(name='eight').first()
print(f"  SchoolClass 'eight': {school_class}")
print(f"  Subjects: {Subject.objects.filter(school_class=school_class).count()}")
print(f"  Timetable: {Timetable.objects.filter(section__school_class=school_class).count()}")
print(f"  Syllabus: {Syllabus.objects.filter(subject__school_class=school_class).count()}")
print(f"  Teachers: {Teacher.objects.count()}")
print("\nAll done!")
