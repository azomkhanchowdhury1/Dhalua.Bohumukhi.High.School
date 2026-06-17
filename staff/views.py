# STAFF_VIEWS_START
from django.shortcuts import render, redirect
from notices.models import Notice
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    LeaveRequest, ProblemReport, InventoryRequest, Staff, DutySchedule,
    AttendanceLog, DirectMessage, TaskAssignment, SalaryPayment,
    Holiday, EmergencyRequest, Document, EventDuty, PerformanceRecord, VisitorLog
)

def dashboard(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return redirect('accounts:login')
        
    try:
        staff_profile = request.user.staff_profile
    except Staff.DoesNotExist:
        staff_profile = None

    if not staff_profile:
        # Fallback if the user is not staff but logged in
        return render(request, 'staff/dashboard.html', {'error': 'Staff profile not found.'})

    if request.method == 'POST':
        action = request.POST.get('action')

        # 1. Leave Request
        if action == 'leave_request':
            leave_type = request.POST.get('leave_type')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            reason = request.POST.get('reason')
            attachment = request.FILES.get('attachment')
            
            LeaveRequest.objects.create(
                staff=staff_profile,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                attachment=attachment
            )
            # Relationship: notify admin of leave request via DM
            admin_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(username='admin').first()
            if admin_user:
                DirectMessage.objects.create(
                    sender=request.user,
                    receiver=admin_user,
                    message=f"Leave Request Submitted: I have applied for {leave_type} from {start_date} to {end_date}."
                )
            messages.success(request, 'Leave Application Submitted Successfully!')
            return redirect('staff:staff_dashboard')

        # 2. Problem Report
        elif action == 'problem_report':
            category = request.POST.get('category')
            description = request.POST.get('description')

            ProblemReport.objects.create(
                staff=staff_profile,
                category=category,
                description=description
            )
            # Relationship: notify admin of problem report via DM
            admin_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(username='admin').first()
            if admin_user:
                DirectMessage.objects.create(
                    sender=request.user,
                    receiver=admin_user,
                    message=f"Problem Report [{category}]: {description}"
                )
            messages.success(request, 'Problem Reported to Admin Successfully!')
            return redirect('staff:staff_dashboard')

        # 3. Inventory Request
        elif action == 'inventory_request':
            items = request.POST.getlist('items')
            quantity = request.POST.get('quantity')
            items_str = ', '.join(items)
            
            InventoryRequest.objects.create(
                staff=staff_profile,
                items=items_str,
                quantity=quantity
            )
            # Relationship: notify admin of inventory request via DM
            admin_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(username='admin').first()
            if admin_user:
                DirectMessage.objects.create(
                    sender=request.user,
                    receiver=admin_user,
                    message=f"Inventory Request: I need {quantity} of {items_str}."
                )
            messages.success(request, 'Inventory Request Sent Successfully!')
            return redirect('staff:staff_dashboard')

        # 4. Send Direct Message
        elif action == 'send_message':
            receiver_id = request.POST.get('receiver_id')
            msg_content = request.POST.get('message')
            
            try:
                receiver = User.objects.get(id=receiver_id)
                DirectMessage.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    message=msg_content
                )
                messages.success(request, 'Message sent successfully!')
            except User.DoesNotExist:
                messages.error(request, 'Recipient user does not exist.')
            return redirect('staff:staff_dashboard')

        # 5. Update Task Status
        elif action == 'update_task_status':
            task_id = request.POST.get('task_id')
            new_status = request.POST.get('status')
            
            try:
                task = TaskAssignment.objects.get(id=task_id, staff=staff_profile)
                task.status = new_status
                task.save()
                # Relationship: if task is completed, log performance evaluation and send DM to admin
                if new_status == 'Completed':
                    PerformanceRecord.objects.create(
                        staff=staff_profile,
                        record_type='Evaluation',
                        title=f"Task Completed: {task.title}",
                        description=f"Successfully completed the assigned task: {task.title}.",
                        date_issued=timezone.now().date()
                    )
                    admin_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(username='admin').first()
                    if admin_user:
                        DirectMessage.objects.create(
                            sender=request.user,
                            receiver=admin_user,
                            message=f"Task Completed: I have completed the task: '{task.title}'."
                        )
                messages.success(request, f'Task status updated to {new_status}!')
            except TaskAssignment.DoesNotExist:
                messages.error(request, 'Task not found.')
            return redirect('staff:staff_dashboard')

        # 6. Profile Info Update
        elif action == 'update_profile':
            phone = request.POST.get('phone_number')
            address = request.POST.get('address')
            
            staff_profile.phone_number = phone
            staff_profile.address = address
            staff_profile.save()
            messages.success(request, 'Contact details updated successfully!')
            return redirect('staff:staff_dashboard')

        # 7. Password Change
        elif action == 'change_password':
            old_pass = request.POST.get('old_password')
            new_pass = request.POST.get('new_password')
            confirm_pass = request.POST.get('confirm_password')
            
            user = request.user
            if not user.check_password(old_pass):
                messages.error(request, 'Incorrect old password.')
            elif new_pass != confirm_pass:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_pass)
                user.save()
                update_session_auth_hash(request, user) # keep logged in
                messages.success(request, 'Password changed successfully!')
            return redirect('staff:staff_dashboard')

        # 8. Emergency Request
        elif action == 'emergency_request':
            title = request.POST.get('title')
            description = request.POST.get('description')
            
            # Create Emergency Request
            EmergencyRequest.objects.create(
                sender=request.user,
                title=title,
                description=description
            )
            # Relationship: also create a school Notice and a TaskAssignment for the staff
            Notice.objects.create(
                title=f"Emergency: {title}",
                content=description,
                is_public=False,
                target_staff=True,
                created_by=request.user
            )
            TaskAssignment.objects.create(
                staff=staff_profile,
                title=f"Emergency Action: {title}",
                description=f"Respond to emergency broadcasted by {request.user.first_name}: {description}",
                status='Ongoing',
                due_date=timezone.now().date()
            )
            messages.success(request, 'Emergency request broadcasted and linked to tasks/notices successfully!')
            return redirect('staff:staff_dashboard')

        # 9. Visitor Entry Log
        elif action == 'log_visitor':
            v_name = request.POST.get('visitor_name')
            purpose = request.POST.get('purpose')
            contact = request.POST.get('contact_number')
            
            VisitorLog.objects.create(
                visitor_name=v_name,
                purpose=purpose,
                contact_number=contact,
                host_staff=staff_profile,
                entry_time=timezone.now()
            )
            messages.success(request, 'Visitor check-in logged successfully!')
            return redirect('staff:staff_dashboard')

        # 10. Visitor Exit Log
        elif action == 'exit_visitor':
            v_id = request.POST.get('visitor_id')
            
            try:
                visitor = VisitorLog.objects.get(id=v_id, host_staff=staff_profile)
                visitor.exit_time = timezone.now()
                visitor.save()
                messages.success(request, 'Visitor check-out logged successfully!')
            except VisitorLog.DoesNotExist:
                messages.error(request, 'Visitor record not found.')
            return redirect('staff:staff_dashboard')

        # 11. Payout / Withdrawal Request
        elif action == 'payout_request':
            from finance.models import PayoutRequest
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
            return redirect('staff:staff_dashboard')

    # --- Fetch Data for Dashboard View ---
    
    # notices
    notices = Notice.objects.filter(Q(is_public=True) | Q(target_staff=True)).distinct().order_by('-created_at')[:5]
    
    # duties
    duties = DutySchedule.objects.filter(staff=staff_profile).order_by('date', 'start_time')
    
    # attendance summary
    attn_logs = AttendanceLog.objects.filter(staff=staff_profile)
    attendance_present = attn_logs.filter(status__in=['Present', 'Late']).count()
    attendance_absent = attn_logs.filter(status='Absent').count()
    attendance_total = attn_logs.count()
    late_entry_report = attn_logs.filter(status='Late').order_by('-date')
    recent_attendance = attn_logs.order_by('-date')[:10]
    
    # leaves and problems
    leave_requests = LeaveRequest.objects.filter(staff=staff_profile).order_by('-created_at')[:5]
    problem_reports = ProblemReport.objects.filter(staff=staff_profile).order_by('-created_at')[:5]
    
    # messaging
    messages_received = DirectMessage.objects.filter(receiver=request.user).order_by('-created_at')
    messages_sent = DirectMessage.objects.filter(sender=request.user).order_by('-created_at')
    all_users = User.objects.exclude(id=request.user.id).order_by('first_name', 'username')
    
    # tasks
    tasks = TaskAssignment.objects.filter(staff=staff_profile).order_by('-due_date')
    
    # salaries
    salaries = SalaryPayment.objects.filter(staff=staff_profile).order_by('-month')
    dues_count = SalaryPayment.objects.filter(staff=staff_profile, status='Unpaid').count()
    
    # holidays
    holidays = Holiday.objects.all().order_by('start_date')
    
    # emergencies
    emergencies = EmergencyRequest.objects.filter(
        Q(target_staff=staff_profile) | Q(target_staff__isnull=True)
    ).order_by('-created_at')
    
    # documents
    documents = Document.objects.all().order_by('title')
    
    # event duties
    event_duties = EventDuty.objects.filter(staff=staff_profile).order_by('event_date')
    
    # performance record
    performance_records = PerformanceRecord.objects.filter(staff=staff_profile).order_by('-date_issued')
    
    # visitors
    visitors = VisitorLog.objects.filter(host_staff=staff_profile).order_by('-entry_time')
    
    # inventory requests
    inventory_requests = InventoryRequest.objects.filter(staff=staff_profile).order_by('-created_at')

    # payout requests
    from finance.models import PayoutRequest
    payout_requests = PayoutRequest.objects.filter(user=request.user).order_by('-requested_at')

    context = {
        'staff_profile': staff_profile,
        'notices': notices,
        'duties': duties,
        'attendance_present': attendance_present,
        'attendance_absent': attendance_absent,
        'attendance_total': attendance_total,
        'late_entry_report': late_entry_report,
        'recent_attendance': recent_attendance,
        'leave_requests': leave_requests,
        'problem_reports': problem_reports,
        'messages_received': messages_received,
        'messages_sent': messages_sent,
        'all_users': all_users,
        'tasks': tasks,
        'salaries': salaries,
        'dues_count': dues_count,
        'holidays': holidays,
        'emergencies': emergencies,
        'documents': documents,
        'event_duties': event_duties,
        'performance_records': performance_records,
        'visitors': visitors,
        'inventory_requests': inventory_requests,
        'payout_requests': payout_requests,
    }
    return render(request, 'staff/dashboard.html', context)
# STAFF_VIEWS_END
