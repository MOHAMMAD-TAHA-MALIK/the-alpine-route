from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Trek, TrekEvent, Comment
from .forms import TrekForm, TrekEventForm


# --- Authentication & User Profile Views ---

def register(request):
    """User registration view with success message."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to The Alpine Route, {user.username}!")
            return redirect('trek_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def change_password(request):
    """Allows authenticated users to change their password."""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('trek_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


@login_required
def profile(request):
    """Displays the user's profile and their joined/created treks."""
    joined_treks = request.user.joined_treks.all().order_by('date')
    created_treks = request.user.created_treks.all().order_by('date')

    return render(request, 'treks/profile.html', {
        'joined_treks': joined_treks,
        'created_treks': created_treks,
    })


# --- Trek Planning & Participation Views ---

def is_guide(user):
    return user.is_staff


@login_required
@user_passes_test(is_guide)
def create_trek(request):
    """Guide-only view to create upcoming treks."""
    if request.method == 'POST':
        form = TrekForm(request.POST)
        if form.is_valid():
            trek = form.save(commit=False)
            trek.created_by = request.user
            trek.save()
            messages.success(request, "Trek created successfully!")
            return redirect('trek_list')
    else:
        form = TrekForm()
    return render(request, 'treks/trek_form.html', {'form': form})


@login_required
@require_POST
def join_trek(request, pk):
    """Allows logged-in users to sign up as a participant for a Trek."""
    trek = get_object_or_404(Trek, pk=pk)
    if trek.is_full:
        messages.error(request, f"Sorry, {trek.title} is already at full capacity.")
    else:
        trek.participants.add(request.user)
        messages.success(request, f"You have joined {trek.title}!")
    return redirect('trek_list')


@login_required
@require_POST
def leave_trek(request, pk):
    """Allows logged-in users to remove themselves from a Trek."""
    trek = get_object_or_404(Trek, pk=pk)
    trek.participants.remove(request.user)
    messages.info(request, f"You have left {trek.title}.")
    return redirect('trek_list')


# --- Trek Event Feed & Community Views ---

def trek_list(request):
    """Main feed displaying all trek events and planned treks with search & filtering."""
    query = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '')

    treks = Trek.objects.all().order_by('date')

    if query:
        treks = treks.filter(destination__icontains=query)
    if difficulty:
        treks = treks.filter(difficulty=difficulty)

    events = TrekEvent.objects.all().order_by('-date')
    return render(request, 'treks/trek_list.html', {
        'treks': treks,
        'events': events,
        'title': 'All Treks',
        'query': query,
        'difficulty': difficulty,
    })


def upcoming_treks(request):
    """Shows only upcoming trek events."""
    today = timezone.now().date()
    events = TrekEvent.objects.filter(date__gte=today).order_by('date')
    return render(request, 'treks/trek_list.html', {'events': events, 'title': 'Upcoming Events'})


def previous_treks(request):
    """Shows past trek events log."""
    today = timezone.now().date()
    events = TrekEvent.objects.filter(date__lt=today).order_by('-date')
    return render(request, 'treks/trek_list.html', {'events': events, 'title': 'Previous Treks Log'})


def trek_detail(request, pk):
    """Detailed single trek event page showing total likes and comments."""
    event = get_object_or_404(TrekEvent, pk=pk)
    is_liked = (
        event.likes.filter(id=request.user.id).exists()
        if request.user.is_authenticated
        else False
    )
    return render(
        request,
        'treks/trek_detail.html',
        {
            'event': event,
            'is_liked': is_liked,
            'total_likes': event.total_likes(),
        },
    )


@login_required
@require_POST
def like_event(request, pk):
    """Toggle likes on a trek event."""
    event = get_object_or_404(TrekEvent, pk=pk)
    if event.likes.filter(id=request.user.id).exists():
        event.likes.remove(request.user)
    else:
        event.likes.add(request.user)
    return redirect('trek_detail', pk=pk)


@login_required
@require_POST
def add_comment(request, pk):
    """Add a user comment to a trek event."""
    event = get_object_or_404(TrekEvent, pk=pk)
    content = request.POST.get('content', '').strip()
    if content:
        Comment.objects.create(trek=event, user=request.user, content=content)
        messages.success(request, "Comment posted successfully!")
    return redirect('trek_detail', pk=pk)


@login_required
@user_passes_test(is_guide)
def create_trek_event(request):
    """Guide-only view to create a community event post."""
    if request.method == 'POST':
        form = TrekEventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event posted successfully!")
            return redirect('trek_list')
    else:
        form = TrekEventForm()
    return render(request, 'treks/event_form.html', {'form': form})