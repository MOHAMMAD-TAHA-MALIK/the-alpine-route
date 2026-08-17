from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from .models import Trek
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
def join_trek(request, pk):
    trek = get_object_or_404(Trek, pk=pk)
    trek.participants.add(request.user)
    return redirect('trek_list')