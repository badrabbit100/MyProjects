import random
import json
from .models import Game


def create_room(username, room_code):
    """ This function create random ship lists and create a room """

    random_ship_list = random.sample(range(1, 49), 10)
    random_opp_list = random.sample(range(50, 99), 10)
    game = Game(game_create=username,
                room_code=room_code,
                ships_creator=random_ship_list,
                ships_opponent=random_opp_list)
    game.save()


def get_game_from_db(room_code):
    """ Request game data from database """

    try:
        game = Game.objects.filter(room_code=room_code)[0]
        return game
    except IndexError:
        return True


def start_room(game, username, room_code):
    """ Function create room or register opponent (Return True), (False) if room was over """

    if game is None:
        create_room(username, room_code)
        return True
    elif game.is_over is True:
        return False
    else:
        register_opponent(username, game)
        return True


def register_opponent(username, game):
    """ Function add data opponent in DataBase """

    if username != game.game_create:
        game.game_opponent = username
        game.save()


def get_used_cells(game):
    """ Function check used cells of players """

    used_cells = game.used_cells
    if used_cells is None or used_cells == '':
        used_cells = []
    return used_cells


def generate_ship_lists(username, game):
    """ Generate ship lists for players """

    if username == game.game_create:
        enemy_ships_list = json.loads(game.ships_opponent)
        my_ship_list = json.loads(game.ships_creator)
    else:
        my_ship_list = json.loads(game.ships_opponent)
        enemy_ships_list = json.loads(game.ships_creator)

    return enemy_ships_list, my_ship_list


def register_player(game, username):
    """ Register player, generate ship lists, create used cell list """

    game_creator = game.game_create
    used_cells = get_used_cells(game)
    ship_lists = generate_ship_lists(username, game)

    return game_creator, used_cells, ship_lists


def finish_a_room(room_code):
    """ Finish room if game was over and player quit """

    game = Game.objects.filter(room_code=room_code)[0]
    game.is_over = True
    game.save()
