from django.db import models
from student.models import Student

class FeeType(models.Model):
    name = models.CharField(max_length=100) # Tuition Fee, Library Fee, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # START: FEETYPE_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: FEETYPE_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.name} ({self.amount})"

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='Paid') # Paid, Pending
    
    # START: FEEPAYMENT_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: FEEPAYMENT_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.student.student_id} - {self.fee_type.name}"

class Expense(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100) # Salary, Utility, Maintenance
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    # START: EXPENSE_REMINDER_FIELDS
    is_remembered = models.BooleanField(default=False)
    reminder_note = models.TextField(blank=True, null=True)
    # END: EXPENSE_REMINDER_FIELDS
    
    def __str__(self):
        return f"{self.title} - {self.amount}"

class PayoutRequest(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('bKash', 'bKash'), ('Bank Transfer', 'Bank Transfer')])
    account_details = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payout for {self.user.username} - {self.amount} ({self.status})"
