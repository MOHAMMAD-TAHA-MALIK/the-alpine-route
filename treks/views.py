from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

from .models import Trek, TrekEvent, Comment
from .forms import TrekForm


def trek_list(request):
    treks = Trek.objects.all().order_by('date')
    return render(request, 'treks/trek_list.html', {'treks': treks})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
            return redirect('trek_list')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


def is_guide(user):
    return user.is_staff


@login_required
@user_passes_test(is_guide)
def create_trek(request):
    if request.method == 'POST':
        form = TrekForm(request.POST)
        if form.is_valid():
            trek = form.save(commit=False)
            trek.created_by = request.user
            trek.save()
            return redirect('trek_list')
    else:
        form = TrekForm()
    return render(request, 'treks/trek_form.html', {'form': form})


@login_required
@require_POST
def join_trek(request, pk):
    trek = get_object_or_404(Trek, pk=pk)
    trek.participants.add(request.user)
    return redirect('trek_list')


def trek_detail(request, pk):
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
        Comment.objects.create(trek=event, user=request.user, content=content)
    return redirect('trek_detail', pk=pk)