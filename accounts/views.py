from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse
from django.db.models import Q
from .models import RegistrationRequest, UserProfile, ContactMessage, SupportTicket
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from prents.models import Parent
from gallery.models import Gallery

# START: GLOBAL_SEARCH_VIEW
@login_required
def global_search(request):
    query = request.GET.get('q', '')
    results = []
    
    if not query:
        return JsonResponse({'results': []})
    
    user = request.user
    
    # Check if user is Admin (Superuser)
    if user.is_superuser:
        # Search Students
        students = Student.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(student_id__icontains=query)
        ).select_related('user')[:5]
        
        # Search Teachers
        teachers = Teacher.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(teacher_id__icontains=query)
        ).select_related('user')[:5]
        
        # Search Staff
        staffs = Staff.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(staff_id__icontains=query)
        ).select_related('user')[:5]
        
        # Search Parents
        parents = Parent.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(parent_id__icontains=query)
        ).select_related('user')[:5]
        
        for s in students:
            results.append({
                'name': f"{s.user.first_name} {s.user.last_name}",
                'role': f"Student ({s.student_id})",
                'url': f"/students/profile/{s.id}/" # Placeholder
            })
        for t in teachers:
            results.append({
                'name': f"{t.user.first_name} {t.user.last_name}",
                'role': f"Teacher ({t.teacher_id})",
                'url': f"/teacher/profile/{t.id}/" # Placeholder
            })
        for st in staffs:
            results.append({
                'name': f"{st.user.first_name} {st.user.last_name}",
                'role': f"Staff ({st.staff_id})",
                'url': f"/staff/profile/{st.id}/" # Placeholder
            })
        for p in parents:
            results.append({
                'name': f"{p.user.first_name} {p.user.last_name}",
                'role': f"Parent ({p.parent_id})",
                'url': f"/parents/profile/{p.id}/" # Placeholder
            })
            
    else:
        # Non-admin users can only search/find their own data
        user_full_name = f"{user.first_name} {user.last_name}"
        
        if query.lower() in user_full_name.lower() or query.lower() in user.username.lower():
            role_display = "Your Profile"
            if hasattr(user, 'student_profile'):
                role_display = f"My Student Profile ({user.student_profile.student_id})"
            elif hasattr(user, 'teacher_profile'):
                role_display = f"My Teacher Profile ({user.teacher_profile.teacher_id})"
            elif hasattr(user, 'staff_profile'):
                role_display = f"My Staff Profile ({user.staff_profile.staff_id})"
            elif hasattr(user, 'parent_profile'):
                role_display = f"My Parent Profile ({user.parent_profile.parent_id})"
                
            results.append({
                'name': user_full_name,
                'role': role_display,
                'url': '/accounts/profile/'
            })

    return JsonResponse({'results': results})
# END: GLOBAL_SEARCH_VIEW

from notices.models import Notice

def home_view(request):
    public_notices = Notice.objects.filter(is_public=True).order_by('-created_at')[:5]
    return render(request, 'home.html', {'public_notices': public_notices})

def about_view(request):
    return render(request, 'about.html')

def academics_view(request):
    return render(request, 'academics.html')

def admission_view(request):
    return render(request, 'admission.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save to DB
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, "Your message has been sent successfully! We will get back to you soon.")
        return redirect('contact')
        
    return render(request, 'contact.html')

def gallery_view(request):
    gallery_items = Gallery.objects.all().order_by('-created_at')
    return render(request, 'gallery.html', {'gallery_items': gallery_items})

def support_view(request):
    if request.method == 'POST' and 'submit_ticket' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        priority = request.POST.get('priority')
        message = request.POST.get('message')
        
        SupportTicket.objects.create(
            name=name,
            email=email,
            subject=subject,
            priority=priority,
            message=message
        )
        messages.success(request, "Support ticket submitted successfully! Our team will contact you soon.")
        return redirect('support')
        
    return render(request, 'support.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        additional_info = request.POST.get('additional_info')
        
        # Check if email already exists
        if RegistrationRequest.objects.filter(email=email).exists():
            messages.error(request, "A registration request with this email already exists.")
            return render(request, 'accounts/register.html')
            
        # Save the request
        RegistrationRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            role=role,
            additional_info=additional_info
        )
        messages.success(request, "Your registration request has been submitted. Please wait for Admin approval via Email.")
        return redirect('accounts:login')
        
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    user = request.user
    role = ""
    profile_data = None
    
    # Identify profile type
    if hasattr(user, 'student_profile'):
        role = "Student"
        profile_data = user.student_profile
    elif hasattr(user, 'teacher_profile'):
        role = "Teacher"
        profile_data = user.teacher_profile
    elif hasattr(user, 'staff_profile'):
        role = "Staff"
        profile_data = user.staff_profile
    elif hasattr(user, 'parent_profile'):
        role = "Parent"
        profile_data = user.parent_profile
        
    if request.method == 'POST':
        # Common Fields
        profile_data.phone_number = request.POST.get('phone_number')
        profile_data.date_of_birth = request.POST.get('date_of_birth')
        profile_data.gender = request.POST.get('gender')
        profile_data.blood_group = request.POST.get('blood_group')
        profile_data.address = request.POST.get('address')
        
        if request.FILES.get('profile_image'):
            profile_data.profile_image = request.FILES.get('profile_image')
            
        # Role Specific Fields
        if role == 'Student':
            profile_data.roll_number = request.POST.get('roll_number')
            profile_data.current_class = request.POST.get('current_class')
            profile_data.section = request.POST.get('section')
        elif role == 'Teacher':
            profile_data.department = request.POST.get('department')
            profile_data.subject = request.POST.get('subject')
            profile_data.qualification = request.POST.get('qualification')
        elif role == 'Staff':
            profile_data.designation = request.POST.get('designation')
            profile_data.department = request.POST.get('department')
        elif role == 'Parent':
            profile_data.occupation = request.POST.get('occupation')
            
        profile_data.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('accounts:profile')
        
    return render(request, 'accounts/profile.html', {
        'role': role,
        'profile': profile_data
    })

@login_required
def settings_view(request):
    if request.method == 'POST':
        current_pw = request.POST.get('current_password')
        new_pw = request.POST.get('new_password')
        confirm_pw = request.POST.get('confirm_password')
        
        user = request.user
        if user.check_password(current_pw):
            if new_pw == confirm_pw:
                user.set_password(new_pw)
                user.save()
                auth_login(request, user) # Re-login to keep session active
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "New passwords do not match.")
        else:
            messages.error(request, "Current password is incorrect.")
        return redirect('accounts:settings')
        
    return render(request, 'accounts/settings.html')

def logout_view(request):
    auth_logout(request)
    return redirect('accounts:login')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'Student'}
            )
            
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            profile.otp_code = otp
            profile.save()
            
            # Send Email
            subject = 'Password Reset OTP - School Management System'
            message = f'Hello {user.first_name},\n\nYour OTP for password reset is: {otp}\n\nDo not share this with anyone.\n\nRegards,\nSchool Admin'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            
            # Save email in session to verify OTP later
            request.session['reset_email'] = email
            messages.success(request, "OTP has been sent to your email.")
            return redirect('accounts:otp_verify')
            
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            
    return render(request, 'accounts/forgot_password.html')

def otp_verify_view(request):
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('accounts:forgot_password')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp_code')
        try:
            user = User.objects.get(email=email)
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'Student'}
            )
            
            if profile.otp_code == otp_entered:
                # OTP is correct
                profile.otp_code = None # Clear OTP
                profile.save()
                
                request.session['otp_verified'] = True
                messages.success(request, "OTP verified successfully. You can now reset your password.")
                return redirect('accounts:reset_password')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('accounts:forgot_password')
            
    return render(request, 'accounts/otp_verify.html', {'email': email})

def reset_password_view(request):
    if not request.session.get('otp_verified'):
        messages.error(request, "Please verify OTP first.")
        return redirect('accounts:forgot_password')
        
    email = request.session.get('reset_email')
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
                # Clear session
                del request.session['reset_email']
                del request.session['otp_verified']
                
                messages.success(request, "Password reset successfully. You can now log in.")
                return redirect('accounts:login')
            except User.DoesNotExist:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'accounts/reset_password.html')
