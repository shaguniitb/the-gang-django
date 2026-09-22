from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from .models import GameRoom, RoomPlayer

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lobby')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def lobby_view(request):
    active_rooms = GameRoom.objects.filter(status='waiting').order_by('-created_at')
    return render(request, 'gang/lobby.html', {'rooms': active_rooms})

@login_required
@require_POST
def create_game_view(request):
    display_name = request.user.profile.get_display_name
    title = request.POST.get('title', f"{display_name}'s Game")
    room = GameRoom.objects.create(title=title, host=request.user)
    RoomPlayer.objects.create(room=room, user=request.user)
    return redirect('game_detail', game_id=room.id)

@login_required
def game_detail_view(request, game_id):
    room = get_object_or_404(GameRoom, id=game_id)
    is_player = RoomPlayer.objects.filter(room=room, user=request.user).exists()
    return render(request, 'gang/game_detail.html', {'room': room, 'is_player': is_player})

@login_required
def join_game_view(request, game_id):
    room = get_object_or_404(GameRoom, id=game_id)

    if room.status != 'waiting':
        messages.error(request, "This game has already started.")
    elif room.player_count() >= 10:
        messages.error(request, "This room is full (max 10 players).")
    else:
        RoomPlayer.objects.get_or_create(room=room, user=request.user)

    return redirect('game_detail', game_id=room.id)

@login_required
def start_game_view(request, game_id):
    room = get_object_or_404(GameRoom, id=game_id)

    if request.user != room.host:
        messages.error(request, "Only the host can start the game.")
    elif not room.can_start():
        messages.error(request, "Game requires between 4 and 10 players to start.")
    else:
        room.status = 'in_progress'
        room.save()
        messages.success(request, "Game started!")

    return redirect('game_detail', game_id=room.id)
