from .models import Message, Game
import json


def save_messages(data):
    """ This function save messages of players """

    username = data['data']['username']
    room_code = data['data']['room_code']
    message = data['data']['message']
    Message.objects.create(username=username, room_code=room_code, message=message)


def save_actions(data):
    """ This function save actions of players """

    room_code = data['data']['room_code']
    cell = int(data['data']['index'])
    game = Game.objects.filter(room_code=room_code)[0]
    try:
        actions = (json.loads(str(game.used_cells)))
    except json.decoder.JSONDecodeError:
        actions = []
    actions.append(cell)
    game.used_cells = actions
    game.save()


def select_type_data(text_data):
    """ Select type of data and save messages or actions """

    data = json.loads(text_data)
    if data['data']['type'] == 'game':
        save_actions(data)
        return True
    elif data['data']['type'] == 'message':
        save_messages(data)
        return False
