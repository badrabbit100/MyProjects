from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Message, Game
from .services import register_player, finish_a_room, get_game_from_db, start_room
from seeab.settings import host

def room_view(request):
    """ Function create Room and register Player or Opponent """

    if request.method == 'POST':
        # Collect data
        username = request.POST.get('username')
        room_code = request.POST.get('room_code')
        game = Game.objects.filter(room_code=room_code).first()
        if start_room(game, username, room_code) is True:
            return redirect(f'/play/{room_code}?username={username}')
        messages.success(request, 'Room was over. \nEnter another Room')
        return redirect('start_view')
    return render(request, 'main/login.html')


def play_view(request, room_code):
    """ Function play view """

    username = request.GET.get('username')
    game = get_game_from_db(room_code)
    if game is True:
        return redirect('start_view')
    # Get messages from DB to recover in chat
    sent_messages = Message.objects.filter(room_code=room_code)[0:25]
    # Add player data in Database, generate ship lists
    player = register_player(game, username)

    context = {'room_code': room_code,
               'game_creator': player[0],
               'enemy_ships': player[2][0],
               'my_ships': player[2][1],
               'username': username,
               'sent_messages': sent_messages,
               'us_cells': player[1],
               'host': host
               }

    return render(request, 'main/game.html', context)


def quit_view(request, room_code):
    """ Finish the Room, Set is_over = True """

    finish_a_room(room_code)
    return redirect('start_view')
