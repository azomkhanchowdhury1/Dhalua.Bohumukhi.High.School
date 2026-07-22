# START: accounts/views.py
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
from django.views.decorators.csrf import csrf_exempt
from .models import RegistrationRequest, UserProfile, ContactMessage, SupportTicket, Testimonial
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from prents.models import Parent
from gallery.models import Gallery

# START: GLOBAL_SEARCH_VIEW
@login_required
def global_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    
    if not query:
        return JsonResponse({'results': []})
    
    user = request.user
    
    # Check role and search
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
                'url': f"/admin-dashboard/students/?search={s.student_id}"
            })
        for t in teachers:
            results.append({
                'name': f"{t.user.first_name} {t.user.last_name}",
                'role': f"Teacher ({t.teacher_id})",
                'url': f"/admin-dashboard/teachers/{t.id}/detail/"
            })
        for st in staffs:
            results.append({
                'name': f"{st.user.first_name} {st.user.last_name}",
                'role': f"Staff ({st.staff_id})",
                'url': f"/admin-dashboard/staff/{st.id}/edit/"
            })
        for p in parents:
            results.append({
                'name': f"{p.user.first_name} {p.user.last_name}",
                'role': f"Parent ({p.parent_id})",
                'url': f"/admin-dashboard/parents/{p.id}/edit/"
            })
            
    elif hasattr(user, 'teacher_profile'):
        # Teachers can search students
        students = Student.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(student_id__icontains=query)
        ).select_related('user')[:5]
        for s in students:
            results.append({
                'name': f"{s.user.first_name} {s.user.last_name}",
                'role': f"Student ({s.student_id})",
                'url': f"/teachers/stats/total-students/?search={s.student_id}"
            })

    elif hasattr(user, 'student_profile'):
        # Students can search teachers
        teachers = Teacher.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) | 
            Q(teacher_id__icontains=query)
        ).select_related('user')[:5]
        for t in teachers:
            results.append({
                'name': f"{t.user.first_name} {t.user.last_name}",
                'role': f"Teacher ({t.teacher_id})",
                'url': "/students/academic/teachers/"
            })
        
        # Search Library Books
        from student.models import LibraryBook
        books = LibraryBook.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(category__icontains=query)
        )[:5]
        for b in books:
            results.append({
                'name': b.title,
                'role': f"Library Book ({b.author})",
                'url': "/students/learning/library/"
            })

    # Search Notices for all logged in users based on targets
    from notices.models import Notice
    notices_query = Q(is_public=True)
    if hasattr(user, 'student_profile'):
        notices_query |= Q(target_student=True)
    elif hasattr(user, 'teacher_profile'):
        notices_query |= Q(target_teacher=True)
    elif hasattr(user, 'staff_profile'):
        notices_query |= Q(target_staff=True)
    elif hasattr(user, 'parent_profile'):
        notices_query |= Q(target_parent=True)

    notices = Notice.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query)
    ).filter(notices_query).distinct()[:5]

    for n in notices:
        results.append({
            'name': n.title,
            'role': f"Notice ({n.created_at.strftime('%d %b')})",
            'url': "/admin-dashboard/notices/" if user.is_superuser else "/notices/"
        })

    # Search Events for all logged in users
    from events.models import Event
    events = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(location__icontains=query)
    )[:5]
    for e in events:
        results.append({
            'name': e.title,
            'role': f"Event ({e.date.strftime('%d %b')})",
            'url': "/admin-dashboard/events/" if user.is_superuser else "/events/"
        })

    # Always return self profile option
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
from events.models import Event
from django.utils import timezone

def home_view(request):
    from django.core.management import call_command
    try:
        call_command('makemigrations', 'teacher')
        call_command('migrate', 'teacher')
    except Exception as e:
        print("Auto-migration failed:", e)

    from accounts.models import Testimonial
    public_notices = Notice.objects.filter(is_public=True).order_by('-created_at')[:5]
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')[:4]
    testimonials = Testimonial.objects.all()[:6]
    return render(request, 'home.html', {
        'public_notices': public_notices,
        'upcoming_events': upcoming_events,
        'testimonials': testimonials,
    })

def about_view(request):
    return render(request, 'about.html')

def academics_view(request):
    from academics.models import Syllabus, ClassRoutine, SchoolClass
    science_syllabuses = Syllabus.objects.filter(group='Science').select_related('subject')
    commerce_syllabuses = Syllabus.objects.filter(group='Commerce').select_related('subject')
    humanities_syllabuses = Syllabus.objects.filter(group='Humanities').select_related('subject')
    # Get all school classes and their routines
    school_classes = SchoolClass.objects.prefetch_related('routines').all()
    routines = ClassRoutine.objects.select_related('school_class').all()
    return render(request, 'academics.html', {
        'science_syllabuses': science_syllabuses,
        'commerce_syllabuses': commerce_syllabuses,
        'humanities_syllabuses': humanities_syllabuses,
        'school_classes': school_classes,
        'routines': routines,
    })

def admission_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '')
        applying_class = request.POST.get('applying_class', '')
        previous_school = request.POST.get('previous_school', '')
        parent_name = request.POST.get('parent_name', '')
        contact_number = request.POST.get('contact_number', '')
        address = request.POST.get('address', '')

        if not email or not full_name:
            messages.error(request, "Full name and email are required.")
            return redirect('admission')

        if RegistrationRequest.objects.filter(email=email).exists():
            messages.error(request, "An application with this email already exists.")
            return redirect('admission')

        # Split name
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        # Prepare additional info
        additional_info = (
            f"Date of Birth: {date_of_birth}\n"
            f"Applying for Class: {applying_class}\n"
            f"Previous School: {previous_school}\n"
            f"Parent's Name: {parent_name}\n"
            f"Address: {address}"
        )

        RegistrationRequest.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=contact_number,
            role='Student',
            additional_info=additional_info,
        )
        messages.success(request, "Your application has been submitted successfully! You will receive login credentials via email after admin approval.")
        return redirect('admission')

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

# START: CHATBOT_VIEW
@csrf_exempt
def chatbot_response(request):
    """
    Smart rule-based chatbot for Dhula High School.
    Supports both English and Bengali queries.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    import json
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
    except Exception:
        user_message = request.POST.get('message', '').strip()

    if not user_message:
        return JsonResponse({'reply': 'দয়া করে একটি প্রশ্ন লিখুন। / Please type a question.'})

    msg = user_message.lower()

    def has(keywords):
        return any(k in msg for k in keywords)

    # ========== GREETINGS ==========
    if has(['hello', 'hi', 'hey', 'হ্যালো', 'হেলো', 'হাই', 'সালাম', 'আসসালামু', 'assalam', 'good morning', 'good afternoon', 'good evening', 'শুভ সকাল', 'শুভ বিকাল']):
        return JsonResponse({'reply': (
            "👋 আস-সালামু আলাইকুম! স্বাগতম ঢুলা উচ্চ বিদ্যালয়ে!\n\n"
            "Hello! Welcome to Dhula High School AI Assistant!\n\n"
            "আমি আপনাকে যা যা বিষয়ে সাহায্য করতে পারি:\n"
            "• 🏫 ভর্তি তথ্য ও ফি (Admission & Fees)\n"
            "• 📝 ফরম পূরণ (Online Application Form)\n"
            "• 📚 সিলেবাস ও কারিকুলাম (Syllabus)\n"
            "• 📅 ক্লাস রুটিন (Class Routine)\n"
            "• 🔐 পাসওয়ার্ড ও একাউন্ট (Password/Account)\n"
            "• 🏛️ স্কুলের ইতিহাস (School History)\n"
            "• 📞 যোগাযোগ (Contact)\n\n"
            "কী জানতে চান?"
        )})

    # ========== FORM / APPLICATION ==========
    if has(['ফরম', 'form', 'আবেদন ফরম', 'apply form', 'application form', 'ফর্ম']):
        return JsonResponse({'reply': (
            "📝 অনলাইন আবেদন ফরম (Online Application Form):\n\n"
            "ধাপ ১: আমাদের Admissions পেজে যান\n"
            "ধাপ ২: 'Online Application Form' পূরণ করুন:\n"
            "  • পূর্ণ নাম (Full Name)\n"
            "  • ইমেইল ঠিকানা (Email — এখানে লগইন তথ্য পাঠানো হবে)\n"
            "  • জন্ম তারিখ (Date of Birth)\n"
            "  • কোন ক্লাসে ভর্তি হতে চান\n"
            "  • আগের স্কুলের নাম\n"
            "  • অভিভাবকের নাম ও মোবাইল নম্বর\n"
            "ধাপ ৩: 'Submit Application' বাটনে ক্লিক করুন\n"
            "ধাপ ৪: Admin অনুমোদন করলে আপনার Email-এ Username ও Password পাঠানো হবে\n\n"
            "👉 Admissions পেজে গিয়ে ফরমটি পূরণ করুন!"
        )})

    # ========== ADMISSION + FEE COMBINED ==========
    if has(['admission', 'ভর্তি', 'applying', 'apply', 'আবেদন', 'ভর্তি হতে']):
        if has(['fee', 'cost', 'amount', 'ফি', 'মূল্য', 'টাকা', 'খরচ', 'fees', '&', 'and']):
            return JsonResponse({'reply': (
                "🏫 ভর্তি তথ্য ও ফি (Admissions & Fees):\n\n"
                "📋 ফি কাঠামো:\n"
                "• ভর্তি ফি: ৳৫,০০০\n"
                "• মাসিক বেতন: ৳১,২০০\n"
                "• লাইব্রেরি ও ল্যাব ফি: ৳১,৫০০/বছর\n"
                "• সহশিক্ষা কার্যক্রম: ৳৮০০/বছর\n\n"
                "📝 আবেদন পদ্ধতি (৪ ধাপ):\n"
                "১. অনলাইন ফরম পূরণ করুন\n"
                "২. ভর্তি পরীক্ষায় অংশ নিন\n"
                "৩. সাক্ষাৎকার (শর্টলিস্টেড প্রার্থীদের জন্য)\n"
                "৪. ফি পরিশোধ ও নথিভুক্তি সম্পন্ন করুন\n\n"
                "📞 আরও জানতে: +880 1607-55120"
            )})

        if has(['requirement', 'eligible', 'eligibility', 'যোগ্যতা', 'প্রয়োজন', 'লাগবে']):
            return JsonResponse({'reply': (
                "📚 ভর্তির যোগ্যতা (Eligibility):\n\n"
                "• ৬ষ্ঠ শ্রেণি: PEC-তে ন্যূনতম GPA ৪.০০\n"
                "• ৯ম শ্রেণি বিজ্ঞান: JSC-তে ন্যূনতম GPA ৪.৫০\n"
                "• ৯ম শ্রেণি বাণিজ্য/মানবিক: JSC-তে ন্যূনতম GPA ৪.০০\n\n"
                "প্রয়োজনীয় কাগজপত্র:\n"
                "• জন্ম নিবন্ধন সনদ\n"
                "• ৪ কপি পাসপোর্ট সাইজ ছবি\n"
                "• আগের স্কুলের ছাড়পত্র (TC)"
            )})

        return JsonResponse({'reply': (
            "🏫 ভর্তি তথ্য (Admission Information):\n\n"
            "✅ ২০২৬-২০২৭ শিক্ষাবর্ষে ভর্তি চলছে!\n\n"
            "• ভর্তি ফি: ৳৫,০০০\n"
            "• মাসিক বেতন: ৳১,২০০\n"
            "• আবেদন: Admissions পেজে অনলাইন ফরম পূরণ করুন\n"
            "• Admin অনুমোদনের পর Email-এ Username ও Password পাবেন\n\n"
            "আরও জানতে চাইলে জিজ্ঞেস করুন:\n"
            "• ভর্তি ফি কত?\n"
            "• ফরম কীভাবে পূরণ করব?\n"
            "• যোগ্যতা কী লাগবে?"
        )})

    # ========== FEE / PAYMENT (standalone) ==========
    if has(['fee', 'ফি', 'payment', 'পেমেন্ট', 'টাকা', 'বেতন', 'মাসিক', 'cost', 'খরচ']):
        return JsonResponse({'reply': (
            "💰 ফি কাঠামো (Fee Structure):\n\n"
            "• ভর্তি ফি: ৳৫,০০০\n"
            "• মাসিক বেতন: ৳১,২০০\n"
            "• লাইব্রেরি ও ল্যাব: ৳১,৫০০/বছর\n"
            "• সহশিক্ষা কার্যক্রম: ৳৮০০/বছর\n\n"
            "শিক্ষার্থীরা Student Portal থেকে পেমেন্ট ইতিহাস দেখতে পারবেন।"
        )})

    # ========== PASSWORD / LOGIN / ACCOUNT ==========
    if has(['password', 'পাসওয়ার্ড', 'login', 'লগইন', 'forgot', 'ভুলে', 'reset', 'otp', 'account', 'একাউন্ট']):
        if has(['forgot', 'reset', 'ভুলে গেছি', 'ভুলে', 'change', 'পরিবর্তন', 'জানি না']):
            return JsonResponse({'reply': (
                "🔐 পাসওয়ার্ড রিসেট (Password Reset):\n\n"
                "ধাপ ১: Login পেজে যান\n"
                "ধাপ ২: 'Forgot Password' লিংকে ক্লিক করুন\n"
                "ধাপ ৩: আপনার নিবন্ধিত Email ঠিকানা লিখুন\n"
                "ধাপ ৪: Email-এ ৬ সংখ্যার OTP কোড পাবেন\n"
                "ধাপ ৫: OTP দিয়ে নতুন পাসওয়ার্ড সেট করুন\n\n"
                "📌 Email না পেলে Spam/Junk ফোল্ডার চেক করুন।"
            )})
        return JsonResponse({'reply': (
            "🔑 একাউন্ট ও লগইন সাহায্য:\n\n"
            "• পাসওয়ার্ড ভুলে গেলে: Login পেজে 'Forgot Password' ক্লিক করুন\n"
            "• নতুন ব্যবহারকারী: Admin অনুমোদনের পর Email-এ তথ্য পাবেন\n"
            "• Username জানতে: Admin অনুমোদনের সময় পাঠানো Email চেক করুন\n"
            "• অন্য সমস্যায়: Support Ticket খুলুন"
        )})

    # ========== CLASS ROUTINE ==========
    if has(['routine', 'রুটিন', 'schedule', 'সময়সূচি', 'timetable', 'time table', 'ক্লাস রুটিন', 'class routine']):
        return JsonResponse({'reply': (
            "📅 ক্লাস রুটিন (Class Routine):\n\n"
            "• Academics পেজে যান\n"
            "• 'Class Routine' সেকশনে স্ক্রল করুন\n"
            "• ড্রপডাউন থেকে আপনার ক্লাস সিলেক্ট করুন (৬ষ্ঠ থেকে ১০ম)\n"
            "• রুটিন দেখুন এবং Download করুন\n\n"
            "📌 রুটিন Admin-এর মাধ্যমে আপলোড ও আপডেট হয়।"
        )})

    # ========== SYLLABUS / CURRICULUM ==========
    if has(['syllabus', 'সিলেবাস', 'curriculum', 'কারিকুলাম', 'subject', 'বিষয়', 'পাঠ্যক্রম']):
        if has(['science', 'বিজ্ঞান']):
            return JsonResponse({'reply': (
                "🔬 বিজ্ঞান গ্রুপ সিলেবাস (Science):\n\n"
                "বিষয়সমূহ: পদার্থ, রসায়ন, জীববিজ্ঞান, উচ্চতর গণিত\n\n"
                "সিলেবাস দেখতে: Academics → Curriculum & Syllabus → Science → View Syllabus\n"
                "সেখান থেকে Download করা যাবে।"
            )})
        if has(['commerce', 'বাণিজ্য', 'ব্যবসা', 'business']):
            return JsonResponse({'reply': (
                "💼 বাণিজ্য গ্রুপ সিলেবাস (Commerce):\n\n"
                "বিষয়সমূহ: হিসাববিজ্ঞান, ফিন্যান্স, ব্যবসায় উদ্যোগ\n\n"
                "সিলেবাস দেখতে: Academics → Curriculum & Syllabus → Commerce → View Syllabus"
            )})
        if has(['humanities', 'মানবিক', 'arts', 'কলা']):
            return JsonResponse({'reply': (
                "🎨 মানবিক গ্রুপ সিলেবাস (Humanities):\n\n"
                "বিষয়সমূহ: ইতিহাস, ভূগোল, পৌরনীতি, অর্থনীতি\n\n"
                "সিলেবাস দেখতে: Academics → Curriculum & Syllabus → Humanities → View Syllabus"
            )})
        return JsonResponse({'reply': (
            "📚 সিলেবাস ও কারিকুলাম (Syllabus & Curriculum):\n\n"
            "আমাদের ৩টি গ্রুপ আছে:\n"
            "• 🔬 বিজ্ঞান — পদার্থ, রসায়ন, জীববিজ্ঞান, উচ্চতর গণিত\n"
            "• 💼 বাণিজ্য — হিসাববিজ্ঞান, ফিন্যান্স, ব্যবসায় উদ্যোগ\n"
            "• 🎨 মানবিক — ইতিহাস, ভূগোল, পৌরনীতি, অর্থনীতি\n\n"
            "Academics পেজে গিয়ে 'View Syllabus' ক্লিক করুন।"
        )})

    # ========== SCHOOL HISTORY ==========
    if has(['history', 'ইতিহাস', 'founded', 'established', 'প্রতিষ্ঠা', 'পুরনো', 'কত বছর', 'when was']):
        return JsonResponse({'reply': (
            "🏛️ ঢুলা উচ্চ বিদ্যালয়ের ইতিহাস:\n\n"
            "• প্রতিষ্ঠা: ১৯৮৫ সাল — মানসম্পন্ন শিক্ষা প্রদানের লক্ষ্যে\n"
            "• ১৯৯৮: বিজ্ঞান বিভাগ চালু হয়\n"
            "• ২০১০: ডিজিটাল ক্যাম্পাস কার্যক্রম শুরু\n"
            "• ২০২৩: জাতীয় শিক্ষা শ্রেষ্ঠত্ব পুরস্কার লাভ\n\n"
            "বর্তমানে: ১৫০০+ শিক্ষার্থী, ১২০+ শিক্ষক, ৯৮% পাসের হার!"
        )})

    # ========== PRINCIPAL ==========
    if has(['principal', 'headmaster', 'প্রধান শিক্ষক', 'প্রিন্সিপাল', 'head master']):
        return JsonResponse({'reply': (
            "👨‍💼 প্রধান শিক্ষক:\n\n"
            "Dr. A. K. M. Rahman\n"
            '"শিক্ষা শুধু একাডেমিক নয়; এটি চরিত্র গঠন, সহনশীলতা এবং সহমর্মিতার বিষয়।"\n\n'
            "কার্যালয়ের সময়: রবি–বৃহস্পতি, সকাল ৯টা – বিকাল ৫টা"
        )})

    # ========== GRADING / EXAM / RESULT ==========
    if has(['grade', 'গ্রেড', 'gpa', 'marks', 'নম্বর', 'exam', 'পরীক্ষা', 'result', 'ফলাফল', 'marking', 'pass']):
        return JsonResponse({'reply': (
            "📊 গ্রেডিং পদ্ধতি (Grading System):\n\n"
            "• A+ (৮০–১০০) → GPA ৫.০০\n"
            "• A  (৭০–৭৯)  → GPA ৪.০০\n"
            "• A- (৬০–৬৯)  → GPA ৩.৫০\n"
            "• B  (৫০–৫৯)  → GPA ৩.০০\n"
            "• C  (৪০–৪৯)  → GPA ২.০০\n"
            "• D  (৩৩–৩৯)  → GPA ১.০০\n"
            "• F  (০–৩২)   → GPA ০.০০\n\n"
            "মূল্যায়ন: সাপ্তাহিক পরীক্ষা (২০%) + অ্যাসাইনমেন্ট (১০%) + অর্ধবার্ষিক (৩০%) + বার্ষিক (৪০%)"
        )})

    # ========== CONTACT ==========
    if has(['contact', 'যোগাযোগ', 'phone', 'ফোন', 'number', 'নম্বর', 'address', 'ঠিকানা', 'office', 'অফিস', 'কল']):
        return JsonResponse({'reply': (
            "📞 যোগাযোগের তথ্য (Contact Information):\n\n"
            "• ফোন: +880 1607-55120\n"
            "• অফিসের সময়: রবি–বৃহস্পতি, সকাল ৯টা – বিকাল ৫টা\n"
            "• Contact পেজে ফর্ম পূরণ করে বার্তা পাঠাতে পারেন\n"
            "• সমস্যার জন্য Support Ticket খুলুন"
        )})

    # ========== STATISTICS ==========
    if has(['student', 'শিক্ষার্থী', 'ছাত্র', 'teacher', 'শিক্ষক', 'award', 'পুরস্কার', 'statistics', 'তথ্য', 'কতজন']):
        return JsonResponse({'reply': (
            "📈 স্কুলের সংক্ষিপ্ত তথ্য:\n\n"
            "• মোট শিক্ষার্থী: ১,৫০০+\n"
            "• মোট শিক্ষক: ১২০+\n"
            "• পাসের হার: ৯৮%\n"
            "• জাতীয় পুরস্কার: ২৫+\n"
            "• প্রতিষ্ঠাকাল: ১৯৮৫\n"
            "• সর্বশেষ পুরস্কার: জাতীয় শিক্ষা শ্রেষ্ঠত্ব পুরস্কার (২০২৩)"
        )})

    # ========== NOTICE / EVENT ==========
    if has(['notice', 'নোটিশ', 'event', 'ইভেন্ট', 'news', 'খবর', 'announcement', 'ঘোষণা']):
        return JsonResponse({'reply': (
            "📢 নোটিশ ও ইভেন্ট:\n\n"
            "• সর্বশেষ নোটিশ Home পেজে দেখানো হয়\n"
            "• লগইন করা ব্যবহারকারীরা তাদের ভূমিকা অনুযায়ী নোটিশ পাবেন\n"
            "• আসন্ন ইভেন্ট Home পেজে প্রদর্শিত হয়"
        )})

    # ========== TECHNICAL ==========
    if has(['technical', 'bug', 'error', 'problem', 'সমস্যা', 'issue', 'not working', 'কাজ করছে না', 'হচ্ছে না']):
        return JsonResponse({'reply': (
            "🛠️ প্রযুক্তিগত সমস্যা:\n\n"
            "• পেজ রিফ্রেশ করুন (Ctrl+F5)\n"
            "• Browser Cache পরিষ্কার করুন\n"
            "• আধুনিক ব্রাউজার ব্যবহার করুন (Chrome, Firefox, Edge)\n"
            "• সমস্যা থাকলে Support Ticket খুলুন\n"
            "• জরুরি: +880 1607-55120"
        )})

    # ========== THANKS ==========
    if has(['thank', 'thanks', 'ধন্যবাদ', 'আপনাকে', 'আপনারে', 'shukriya']):
        return JsonResponse({'reply': "😊 স্বাগতম! আর কিছু জানার থাকলে জিজ্ঞেস করুন। / You're welcome! Feel free to ask anything else!"})

    # ========== WHAT CAN YOU DO ==========
    if has(['what can', 'কী কী', 'কি করতে', 'কি বলতে', 'help', 'সাহায্য', 'সহায়তা']):
        return JsonResponse({'reply': (
            "🤖 আমি আপনাকে যা যা বিষয়ে সাহায্য করতে পারি:\n\n"
            "• 📝 ফরম পূরণ ও আবেদন\n"
            "• 🏫 ভর্তি তথ্য ও ফি\n"
            "• 📚 সিলেবাস (বিজ্ঞান/বাণিজ্য/মানবিক)\n"
            "• 📅 ক্লাস রুটিন (৬ষ্ঠ–১০ম শ্রেণি)\n"
            "• 🔐 পাসওয়ার্ড রিসেট ও একাউন্ট সমস্যা\n"
            "• 🏛️ স্কুলের ইতিহাস ও তথ্য\n"
            "• 📊 গ্রেডিং পদ্ধতি\n"
            "• 📞 যোগাযোগ তথ্য\n\n"
            "যেকোনো একটি বিষয়ে জিজ্ঞেস করুন!"
        )})

    # ========== DEFAULT FALLBACK ==========
    return JsonResponse({'reply': (
        "🤖 আমি আপনার প্রশ্নটি বুঝতে পারিনি।\n\n"
        "আপনি এভাবে জিজ্ঞেস করতে পারেন:\n"
        "• 'ভর্তি ফি কত?' বা 'admission fee'\n"
        "• 'ফরম কীভাবে পূরণ করব?' বা 'how to fill form'\n"
        "• 'ক্লাস রুটিন' বা 'class routine'\n"
        "• 'পাসওয়ার্ড ভুলে গেছি' বা 'forgot password'\n"
        "• 'সিলেবাস' বা 'syllabus'\n\n"
        "অথবা Support Ticket খুলুন বিস্তারিত সাহায্যের জন্য।"
    )})
# END: CHATBOT_VIEW


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
    role = "Admin" if user.is_superuser else ""
    profile_data = None
    user_profile = None

    if hasattr(user, 'profile'):
        user_profile = user.profile

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
    elif user.is_superuser:
        role = "Admin"
        profile_data = user_profile

    return render(request, 'accounts/profile.html', {
        'role': role,
        'profile': profile_data,
        'user_profile': user_profile
    })

@login_required
def settings_view(request):
    user = request.user
    role = "Admin" if user.is_superuser else ""
    profile_data = None
    
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
    elif user.is_superuser:
        role = "Admin"
        profile_data = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # --- Save User model fields (only if not empty) ---
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()

            # --- Save UserProfile (phone, image, remember me) ---
            if hasattr(user, 'profile'):
                phone = request.POST.get('phone_number', '').strip()
                if phone:
                    user.profile.phone_number = phone
                user.profile.is_remembered = request.POST.get('is_remembered') == 'on'
                if request.FILES.get('profile_image'):
                    user.profile.profile_image = request.FILES.get('profile_image')
                user.profile.save()

            # --- Save role-specific profile (Student/Teacher/Staff/Parent) ---
            if profile_data and role != 'Admin':
                phone = request.POST.get('phone_number', '').strip()
                if phone:
                    profile_data.phone_number = phone

                dob = request.POST.get('date_of_birth', '').strip()
                if dob and hasattr(profile_data, 'date_of_birth'):
                    profile_data.date_of_birth = dob

                gender = request.POST.get('gender', '').strip()
                if gender and hasattr(profile_data, 'gender'):
                    profile_data.gender = gender

                blood_group = request.POST.get('blood_group', '').strip()
                if hasattr(profile_data, 'blood_group'):
                    profile_data.blood_group = blood_group

                address = request.POST.get('address', '').strip()
                if hasattr(profile_data, 'address'):
                    profile_data.address = address

                if request.FILES.get('profile_image') and hasattr(profile_data, 'profile_image'):
                    profile_data.profile_image = request.FILES.get('profile_image')

                if role == 'Student':
                    # Student's academic fields (roll_number, current_class, section) are read-only
                    pass
                elif role == 'Teacher':
                    dept = request.POST.get('department', '').strip()
                    if dept:
                        profile_data.department = dept
                    subj = request.POST.get('subject', '').strip()
                    if subj:
                        profile_data.subject = subj
                    qual = request.POST.get('qualification', '').strip()
                    if qual:
                        profile_data.qualification = qual
                elif role == 'Staff':
                    desig = request.POST.get('designation', '').strip()
                    if desig and hasattr(profile_data, 'designation'):
                        profile_data.designation = desig
                    dept = request.POST.get('department', '').strip()
                    if dept and hasattr(profile_data, 'department'):
                        profile_data.department = dept
                elif role == 'Parent':
                    occ = request.POST.get('occupation', '').strip()
                    if occ and hasattr(profile_data, 'occupation'):
                        profile_data.occupation = occ

                profile_data.save()

            # --- Also save admin profile fields if Admin ---
            if role == 'Admin' and hasattr(user, 'profile'):
                phone = request.POST.get('phone_number', '').strip()
                if phone:
                    user.profile.phone_number = phone
                dob = request.POST.get('date_of_birth', '').strip()
                if dob:
                    user.profile.date_of_birth = dob
                gender = request.POST.get('gender', '').strip()
                if gender:
                    user.profile.gender = gender
                blood_group = request.POST.get('blood_group', '').strip()
                user.profile.blood_group = blood_group
                address = request.POST.get('address', '').strip()
                user.profile.address = address
                if request.FILES.get('profile_image'):
                    user.profile.profile_image = request.FILES.get('profile_image')
                user.profile.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:settings')

        elif action == 'change_password':
            current_pw = request.POST.get('current_password')
            new_pw = request.POST.get('new_password')
            confirm_pw = request.POST.get('confirm_password')
            
            if user.check_password(current_pw):
                if new_pw == confirm_pw:
                    user.set_password(new_pw)
                    user.save()
                    
                    if hasattr(user, 'student_profile'):
                        user.student_profile.password_plain = new_pw
                        user.student_profile.save()
                    elif hasattr(user, 'teacher_profile'):
                        user.teacher_profile.password_plain = new_pw
                        user.teacher_profile.save()
                    elif hasattr(user, 'staff_profile'):
                        user.staff_profile.password_plain = new_pw
                        user.staff_profile.save()
                    elif hasattr(user, 'parent_profile'):
                        user.parent_profile.password_plain = new_pw
                        user.parent_profile.save()
                        
                    auth_login(request, user) # Re-login to keep session active
                    messages.success(request, "Password updated successfully!")
                else:
                    messages.error(request, "New passwords do not match.")
            else:
                messages.error(request, "Current password is incorrect.")
            return redirect('accounts:settings')

        elif action == 'delete_account':
            if user.is_superuser:
                user.delete()
                messages.success(request, "Your account has been deleted successfully.")
                return redirect('accounts:login')
            else:
                messages.error(request, "Access Denied: Only administrators can delete accounts.")
                return redirect('accounts:settings')

    return render(request, 'accounts/settings.html', {
        'role': role,
        'profile': profile_data,
        'user_profile': user.profile if hasattr(user, 'profile') else None
    })

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
                
                if hasattr(user, 'student_profile'):
                    user.student_profile.password_plain = new_password
                    user.student_profile.save()
                elif hasattr(user, 'teacher_profile'):
                    user.teacher_profile.password_plain = new_password
                    user.teacher_profile.save()
                elif hasattr(user, 'staff_profile'):
                    user.staff_profile.password_plain = new_password
                    user.staff_profile.save()
                elif hasattr(user, 'parent_profile'):
                    user.parent_profile.password_plain = new_password
                    user.parent_profile.save()
                
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

# END: accounts/views.py
