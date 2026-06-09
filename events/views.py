from django.shortcuts import render
from .models import Event
from django.utils import timezone

def event_list_view(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date', 'time')
    past_events = Event.objects.filter(date__lt=today).order_by('-date', '-time')
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'events/event_list.html', context)
