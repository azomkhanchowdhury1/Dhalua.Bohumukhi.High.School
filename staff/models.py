# STAFF_MODELS_START
from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile', null=True, blank=True)
    profile_image = models.ImageField(upload_to='staff/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    staff_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    work_shift = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name} ({self.staff_id})"
        return f"Staff {self.staff_id or self.id}"

class LeaveRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to='staff_leaves/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.leave_type} ({self.status})"

class ProblemReport(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='problem_reports')
    category = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Solved', 'Solved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.category} ({self.status})"

class InventoryRequest(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='inventory_requests')
    items = models.TextField() 
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.items} ({self.status})"

# --- New Models Supporting Staff Dashboard Operations ---

class DutySchedule(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='duty_schedules')
    duty_type = models.CharField(max_length=50, choices=[('Regular', 'Regular'), ('Roster', 'Roster'), ('Special', 'Special')])
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.staff.user.username if self.staff.user else 'Staff'} - {self.title} ({self.duty_type})"

class AttendanceLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='attendance_logs')
    date = models.DateField()
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')])

    def __str__(self):
        return f"{self.staff.user.username if self.staff.user else 'Staff'} - {self.date}: {self.status}"

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.message[:20]}"

class TaskAssignment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed')], default='Pending')
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

class SalaryPayment(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='salaries')
    month = models.CharField(max_length=50) # e.g., 'November 2026'
    payment_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    dues = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.staff.user.username if self.staff.user else 'Staff'} - {self.month} ({self.status})"

class Holiday(models.Model):
    title = models.CharField(max_length=255)
    holiday_type = models.CharField(max_length=50, choices=[('Government', 'Government'), ('School', 'School'), ('Special', 'Special')])
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.holiday_type})"

class EmergencyRequest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emergencies')
    target_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='received_emergencies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=100, choices=[('Joining Letter', 'Offer / Joining Letter'), ('Instruction', 'Duty / Instruction Docs'), ('Form', 'Download Forms')])
    file = models.FileField(upload_to='staff_documents/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.doc_type})"

class EventDuty(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='event_duties')
    event_name = models.CharField(max_length=100, choices=[('Annual Sports', 'Annual Sports'), ('Cultural Program', 'Cultural Program'), ('Parents Meeting Duty', 'Parents Meeting Duty')])
    role_description = models.TextField()
    event_date = models.DateField()
    time_slot = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.staff.user.username if self.staff.user else 'Staff'} - {self.event_name}"

class PerformanceRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='performance_records')
    record_type = models.CharField(max_length=50, choices=[('Evaluation', 'Work Evaluation'), ('Award', 'Staff of the Month'), ('Warning', 'Warnings / Notices')])
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_issued = models.DateField()

    def __str__(self):
        return f"{self.staff.user.username if self.staff.user else 'Staff'} - {self.title} ({self.record_type})"

class VisitorLog(models.Model):
    visitor_name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    host_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='visitor_logs')
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.visitor_name} visited {self.host_staff.user.username if self.host_staff.user else 'Staff'}"

# STAFF_MODELS_END
