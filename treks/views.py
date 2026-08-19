from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Exists, OuterRef

from .models import Trek, TrekEvent, Comment, TrekImage, TrekEventImage
from .forms import TrekForm, TrekEventForm


# Guard function: strictly checks if user is authenticated staff
def is_staff_user(user):
    return user.is_authenticated and user.is_staff


# --- Authentication & User Profile Views ---

def register(request):
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
    joined_treks = request.user.joined_treks.all().prefetch_related('images').order_by('date')
    created_treks = request.user.created_treks.all().prefetch_related('images').order_by('date')

    return render(request, 'treks/profile.html', {
        'joined_treks': joined_treks,
        'created_treks': created_treks,
    })


# --- Trek Planning & Event Creation (STAFF ONLY) ---

@login_required
@user_passes_test(is_staff_user, login_url='trek_list')
def create_trek(request):
    """STAFF ONLY view to create upcoming treks with up to 3 images."""
    if request.method == 'POST':
        form = TrekForm(request.POST, request.FILES)
        if form.is_valid():
            trek = form.save(commit=False)
            trek.created_by = request.user
            trek.save()

            # Process up to 3 uploaded images via custom MultipleFileInput
            images = request.FILES.getlist('images')
            for img in images[:3]:
                TrekImage.objects.create(trek=trek, image=img)

            messages.success(request, "Trek created successfully!")
            return redirect('trek_list')
    else:
        form = TrekForm()
    return render(request, 'treks/trek_form.html', {'form': form})


@login_required
@user_passes_test(is_staff_user, login_url='trek_list')
def create_trek_event(request):
    """STAFF ONLY view to create a community event post with up to 3 images."""
    if request.method == 'POST':
        form = TrekEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()

            # Process up to 3 uploaded images
            images = request.FILES.getlist('images')
            for img in images[:3]:
                TrekEventImage.objects.create(event=event, image=img)

            messages.success(request, "Event posted successfully!")
            return redirect('trek_list')
    else:
        form = TrekEventForm()
    return render(request, 'treks/event_form.html', {'form': form})


# --- Participation & Community Actions (ALL USERS) ---

@login_required
@require_POST
def join_trek(request, pk):
    trek = get_object_or_404(Trek, pk=pk)
    if trek.created_by == request.user:
        messages.error(request, "You can't join a trek you organized.")
        return redirect('trek_list')
    if trek.participants.filter(pk=request.user.pk).exists():
        messages.info(request, "You're already in this trek.")
        return redirect('trek_list')
    if trek.is_full:
        messages.error(request, f"Sorry, {trek.title} is already at full capacity.")
    else:
        trek.participants.add(request.user)
        messages.success(request, f"You have joined {trek.title}!")
    return redirect('trek_list')


@login_required
@require_POST
def leave_trek(request, pk):
    trek = get_object_or_404(Trek, pk=pk)
    trek.participants.remove(request.user)
    messages.info(request, f"You have left {trek.title}.")
    return redirect('trek_list')


def trek_list(request):
    query = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '')

    # Build the subquery ONLY if user is logged in
    if request.user.is_authenticated:
        user_joined_subquery = Trek.participants.through.objects.filter(
            trek_id=OuterRef('pk'),
            user_id=request.user.pk
        )
        treks = Trek.objects.prefetch_related('images', 'participants') \
                            .annotate(user_has_joined=Exists(user_joined_subquery)) \
                            .order_by('date')
    else:
        treks = Trek.objects.prefetch_related('images', 'participants') \
                            .order_by('date')

    if query:
        treks = treks.filter(destination__icontains=query)
    if difficulty:
        treks = treks.filter(difficulty=difficulty)

    events = TrekEvent.objects.prefetch_related('images', 'likes').all().order_by('-date')

    return render(request, 'treks/trek_list.html', {
        'treks': treks,
        'events': events,
        'title': 'All Treks',
        'query': query,
        'difficulty': difficulty,
    })


def upcoming_treks(request):
    
    today = timezone.now().date()
    treks = Trek.objects.prefetch_related('images', 'participants') \
                .filter(date__gte=today).order_by('date')
    return render(request, 'treks/trek_list.html', {
        'treks': treks,
        'title': 'Upcoming Treks'
    })

def previous_treks(request):
    today = timezone.now().date()
    treks = Trek.objects.prefetch_related('images', 'participants') \
                .filter(date__lt=today).order_by('-date')
    return render(request, 'treks/trek_list.html', {
        'treks': treks,
        'title': 'Past Treks'
    })


def trek_detail(request, pk):
    event = get_object_or_404(
        TrekEvent.objects.prefetch_related('images', 'comments__user', 'likes'), 
        pk=pk
    )
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
    event = get_object_or_404(TrekEvent, pk=pk)
    if event.likes.filter(id=request.user.id).exists():
        event.likes.remove(request.user)
    else:
        event.likes.add(request.user)
    return redirect('trek_detail', pk=pk)


@login_required
@require_POST
def add_comment(request, pk):
    event = get_object_or_404(TrekEvent, pk=pk)
    content = request.POST.get('content', '').strip()
    if content:
        # Changed event=event to trek=event to align with Comment model's FK name
        Comment.objects.create(trek=event, user=request.user, content=content)
        messages.success(request, "Comment posted successfully!")
    else:
        messages.error(request, "Comment cannot be empty.")
    return redirect('trek_detail', pk=pk)