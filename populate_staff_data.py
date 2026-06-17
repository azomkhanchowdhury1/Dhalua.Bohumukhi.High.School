# SEEDING_SCRIPT_START
import os
import django
import datetime
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setting.settings')
django.setup()

from django.contrib.auth.models import User
from staff.models import (
    Staff, LeaveRequest, ProblemReport, InventoryRequest, DutySchedule,
    AttendanceLog, DirectMessage, TaskAssignment, SalaryPayment,
    Holiday, EmergencyRequest, Document, EventDuty, PerformanceRecord, VisitorLog
)
from notices.models import Notice

def seed_data():
    print("Starting database seeding for staff operations...")

    # 1. Create or get Admin user
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        admin_user = User.objects.create_superuser('admin', 'admin@school.com', 'admin123')
        print("Created superuser: admin (password: admin123)")

    # 2. Create or get Mr. Rahim
    rahim_user = User.objects.filter(username='rahim').first()
    if not rahim_user:
        rahim_user = User.objects.create_user('rahim', 'rahim@school.com', 'rahim123', first_name='Rahim', last_name='Ahmed')
        print("Created user: rahim")
    
    rahim_staff, _ = Staff.objects.get_or_create(
        user=rahim_user,
        defaults={
            'staff_id': 'STF002',
            'designation': 'Assistant Teacher',
            'department': 'Science',
            'salary': 25000.00,
            'work_shift': 'Morning'
        }
    )

    # 3. Ensure we have at least one test staff member to link items to
    staff_profile = Staff.objects.first()
    if not staff_profile:
        # Create a default staff user
        staff_user = User.objects.create_user('staff', 'staff@school.com', 'staff123', first_name='Jamil', last_name='Hasan')
        staff_profile = Staff.objects.create(
            user=staff_user,
            staff_id='STF001',
            designation='Office Assistant',
            department='Administration',
            joining_date=datetime.date(2025, 1, 1),
            salary=20000.00,
            work_shift='General'
        )
        print("Created default staff user: staff (password: staff123)")
    else:
        print("Using existing staff profile found in database.")

    staff_user = staff_profile.user

    # 4. Notice Board
    Notice.objects.get_or_create(
        title="Urgent Staff Meeting",
        defaults={
            'content': "All staff members are requested to attend an urgent meeting today at 2:00 PM in the conference room. Subject: Upcoming academic evaluation.",
            'is_public': False,
            'target_staff': True,
            'created_by': admin_user
        }
    )
    Notice.objects.get_or_create(
        title="Annual Exam Routine",
        defaults={
            'content': "The official routine for the Annual Exam 2026 has been published. Please download the attachment and coordinate classes accordingly.",
            'is_public': True,
            'target_staff': True,
            'created_by': admin_user
        }
    )

    # 5. Duty Schedule
    DutySchedule.objects.get_or_create(
        staff=staff_profile,
        title="Regular: Weekly / Monthly Roster",
        defaults={
            'duty_type': 'Roster',
            'description': 'Weekly general administration support roster.',
            'start_time': datetime.time(8, 0),
            'end_time': datetime.time(16, 0),
        }
    )
    DutySchedule.objects.get_or_create(
        staff=staff_profile,
        title="Special Duty (Exam/Event)",
        defaults={
            'duty_type': 'Special',
            'description': 'Hall monitor and room assignment management duty for terminal exams.',
            'start_time': datetime.time(9, 0),
            'end_time': datetime.time(13, 0),
            'date': datetime.date.today()
        }
    )

    # 6. Attendance Log
    # Seed 22 Present logs and 2 Absent logs for dashboard stats
    today = datetime.date.today()
    for i in range(1, 25):
        date_val = today - datetime.timedelta(days=i)
        # Avoid duplicate seeding for the same date
        if not AttendanceLog.objects.filter(staff=staff_profile, date=date_val).exists():
            status = 'Present' if i <= 22 else 'Absent'
            check_in = datetime.time(7, 55) if status == 'Present' else None
            # Make one entry Late to support late entry report
            if i == 5:
                status = 'Late'
                check_in = datetime.time(8, 30) # late entry after 8:00 AM
            
            AttendanceLog.objects.create(
                staff=staff_profile,
                date=date_val,
                check_in_time=check_in,
                check_out_time=datetime.time(16, 0) if status in ['Present', 'Late'] else None,
                status=status
            )

    # 7. Direct Messaging
    DirectMessage.objects.get_or_create(
        sender=admin_user,
        receiver=staff_user,
        message="Need files for the regulatory inspection. Please drop them off at my desk.",
        defaults={'is_read': False}
    )
    DirectMessage.objects.get_or_create(
        sender=rahim_user,
        receiver=staff_user,
        message="Bring chalk and markers to Room 102 when you get a chance.",
        defaults={'is_read': False}
    )

    # 8. Task Assignment
    TaskAssignment.objects.get_or_create(
        staff=staff_profile,
        title="Deliver office files",
        defaults={
            'description': 'Deliver files to Nangalkot Upazila Education Office.',
            'status': 'Ongoing',
            'due_date': today + datetime.timedelta(days=2)
        }
    )
    TaskAssignment.objects.get_or_create(
        staff=staff_profile,
        title="Meeting preparation",
        defaults={
            'description': 'Set up projectors, seats, and folders for the annual committee meeting.',
            'status': 'Completed',
            'due_date': today - datetime.timedelta(days=1)
        }
    )

    # 9. Salary Information
    # Nov Salary Paid: 01 Dec
    SalaryPayment.objects.get_or_create(
        staff=staff_profile,
        month="November 2026",
        defaults={
            'payment_date': datetime.date(2026, 12, 1),
            'amount': staff_profile.salary or 20000.00,
            'status': 'Paid',
            'dues': 0.00
        }
    )
    # View Dues
    SalaryPayment.objects.get_or_create(
        staff=staff_profile,
        month="December 2026",
        defaults={
            'amount': staff_profile.salary or 20000.00,
            'status': 'Unpaid',
            'dues': 1500.00 # showing some unpaid dues
        }
    )

    # 10. Holiday Calendar
    Holiday.objects.get_or_create(
        title="Victory Day",
        defaults={
            'holiday_type': 'Government',
            'start_date': datetime.date(2026, 12, 16),
            'end_date': datetime.date(2026, 12, 16),
            'description': 'National Victory Day celebrations.'
        }
    )
    Holiday.objects.get_or_create(
        title="Summer Vacation",
        defaults={
            'holiday_type': 'School',
            'start_date': datetime.date(2026, 7, 1),
            'end_date': datetime.date(2026, 7, 10),
            'description': 'Annual school summer recess.'
        }
    )
    Holiday.objects.get_or_create(
        title="Annual Exam Preparatory Leaves",
        defaults={
            'holiday_type': 'Special',
            'start_date': datetime.date(2026, 11, 20),
            'end_date': datetime.date(2026, 11, 22),
            'description': 'Special days for exam preparation activities.'
        }
    )

    # 11. Emergency Request
    EmergencyRequest.objects.get_or_create(
        title="Come to Office Quickly!",
        sender=admin_user,
        defaults={
            'description': 'Principal needs assistance with printing urgent inspection documents immediately.',
            'target_staff': staff_profile
        }
    )
    EmergencyRequest.objects.get_or_create(
        title="Bring projector to Room 5",
        sender=rahim_user,
        defaults={
            'description': 'Need the school projector for class presentation in Room 5.',
            'target_staff': staff_profile
        }
    )

    # 12. Document Center
    Document.objects.get_or_create(
        title="Offer / Joining Letter",
        defaults={
            'doc_type': 'Joining Letter',
        }
    )
    Document.objects.get_or_create(
        title="Duty / Instruction Docs",
        defaults={
            'doc_type': 'Instruction',
        }
    )
    Document.objects.get_or_create(
        title="Download Forms",
        defaults={
            'doc_type': 'Form',
        }
    )

    # 13. Event Duty
    EventDuty.objects.get_or_create(
        staff=staff_profile,
        event_name="Annual Sports",
        defaults={
            'role_description': 'Coordinates fields setup and prize distribution rosters.',
            'event_date': today + datetime.timedelta(days=30),
            'time_slot': '09:00 AM - 05:00 PM'
        }
    )
    EventDuty.objects.get_or_create(
        staff=staff_profile,
        event_name="Cultural Program",
        defaults={
            'role_description': 'Sound check assistant and light controller.',
            'event_date': today + datetime.timedelta(days=15),
            'time_slot': '02:00 PM - 08:00 PM'
        }
    )
    EventDuty.objects.get_or_create(
        staff=staff_profile,
        event_name="Parents Meeting Duty",
        defaults={
            'role_description': 'Visitor welcome desk and attendance log compilation.',
            'event_date': today + datetime.timedelta(days=5),
            'time_slot': '10:00 AM - 02:00 PM'
        }
    )

    # 14. Performance Record
    PerformanceRecord.objects.get_or_create(
        staff=staff_profile,
        record_type='Evaluation',
        title="Work Evaluation",
        defaults={
            'description': 'Excellent support during national day preparations. Rated 4.8/5.0.',
            'date_issued': today - datetime.timedelta(days=15)
        }
    )
    PerformanceRecord.objects.get_or_create(
        staff=staff_profile,
        record_type='Award',
        title="Staff of the Month",
        defaults={
            'description': 'Awarded Staff of the Month for outstanding commitment and support.',
            'date_issued': today - datetime.timedelta(days=45)
        }
    )
    PerformanceRecord.objects.get_or_create(
        staff=staff_profile,
        record_type='Warning',
        title="Warnings / Notices",
        defaults={
            'description': 'Reminder regarding late entries in past weeks. Ensure timely reporting.',
            'date_issued': today - datetime.timedelta(days=6)
        }
    )

    # 15. Visitor Management
    VisitorLog.objects.get_or_create(
        visitor_name="Jahir Uddin",
        purpose="Student Admission Query",
        contact_number="01876543210",
        host_staff=staff_profile,
        entry_time=timezone.now() - datetime.timedelta(hours=2),
        defaults={
            'exit_time': timezone.now() - datetime.timedelta(hours=1)
        }
    )
    VisitorLog.objects.get_or_create(
        visitor_name="Rahima Khatun",
        purpose="Parent Teacher Meetup",
        contact_number="01555443322",
        host_staff=staff_profile,
        entry_time=timezone.now()
    )

    # 16. Inventory Request (Marker & Chalks, Cleaning Supplies)
    InventoryRequest.objects.get_or_create(
        staff=staff_profile,
        items="Marker & Chalks",
        defaults={
            'quantity': 3,
            'status': 'Approved'
        }
    )
    InventoryRequest.objects.get_or_create(
        staff=staff_profile,
        items="Cleaning Supplies",
        defaults={
            'quantity': 2,
            'status': 'Pending'
        }
    )

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
# SEEDING_SCRIPT_END
