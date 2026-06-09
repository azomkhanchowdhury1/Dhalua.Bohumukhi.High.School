from django.contrib import admin
from .models import FeeType, FeePayment, Expense

# START: FEETYPE_ADMIN
@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'is_remembered')
    search_fields = ('name',)
    list_filter = ('is_remembered',)
    fieldsets = (
        ('Fee Information', {
            'fields': (('name', 'amount'),)
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: FEETYPE_ADMIN

# START: FEEPAYMENT_ADMIN
@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount_paid', 'status', 'transaction_id', 'payment_date')
    search_fields = ('student__student_id', 'student__user__first_name', 'transaction_id')
    list_filter = ('status', 'fee_type', 'is_remembered')
    fieldsets = (
        ('Payment Information', {
            'fields': (
                ('student', 'fee_type'),
                ('amount_paid', 'status'),
                'transaction_id'
            )
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: FEEPAYMENT_ADMIN

# START: EXPENSE_ADMIN
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'amount', 'date', 'is_remembered')
    search_fields = ('title', 'category')
    list_filter = ('category', 'date', 'is_remembered')
    fieldsets = (
        ('Expense Information', {
            'fields': (
                ('title', 'category'),
                ('amount', 'date'),
                'description'
            )
        }),
        ('Settings', {
            'fields': (('is_remembered', 'reminder_note'),)
        }),
    )
# END: EXPENSE_ADMIN
