# -*- coding: utf-8 -*-
__author__ = 'Andrzej'

import websocket, simplejson as json, requests, re, pogodynka, numbers_game, switch, random

token = 'xoxb-16407766775-cCirwYjEX0IMKIs973FqxDCu'  # Alfred token
users_list = {}
all_channels = {}
welcomed_users = {}
message_identifier = 1
game_in_play = False
player = ""
some_bullshit = ("Daj mi juz spokoj ", "Ile Ci to mozna powtarzac ", "Znowu ", "Jestem juz tym zmeczony ", "Skoncz ", "Przynudzasz ", "Idz sprawdz czy Cie nie ma w drugim pokoju ", "Slucham ", "Zawsze do uslug ", "Jak moge pomoc ")


def send_message_via_ws(ws, type, text, channel):
    global message_identifier
    ws.send(json.dumps({"id": message_identifier,
                        "type": type,
                        "text": text,
                        "channel": channel}))
    message_identifier += 1


def say_hello(ws, user, channel):
    global message_identifier
    if user == "U0FBFBMDW":
        send_message_via_ws(ws, "message", "Witaj Panie! Czym mogę Ci slużyć?\n *!help* jeśliś niezdecydowany", channel)
    else:
        send_message_via_ws(ws, "message", "Hej " + users_list[user] + "\n Wpisz *!help* aby dowiedziec sie wiecej",
                            channel)


def provide_help(ws, channel):
    send_message_via_ws(ws, "message",
                        "Potrafie: \n *!pogoda nazwa_miasta* powiem Ci jaka jest pogoda w wybranym miescie", channel)


def provide_weather(ws, city, channel):
    import pogodynka
    pogodynka.units = "metric"
    json = pogodynka.get_json_for_city(city, "pl", "metric")
    send_message_via_ws(ws, "message", pogodynka.return_parsed_json(json, pogodynka.check_match(json, city)), channel)


def init_number_game(ws, user, channel):
    numbers_game.init_game()
    send_message_via_ws(ws, "message",
                        "Zaczynajmy wiec... Sprobuj odgadnac liczbe z przedzialu 1-100 .. *!koniec* aby sie poddac " + user,
                        channel)


def say_some_bullshit(ws, user, channel):
    global message_identifier
    send_message_via_ws(ws, "message", random.choice(some_bullshit) + users_list[user] ,
                            channel)

def on_message(ws, message):
    message = json.loads(message)
    if 'user' in message and message["type"] == "message":
        if "hej" in message["text"].lower() or "alfred" in message["text"].lower():
            if (("reply_to" in message and message["reply_to"] < message_identifier) or "reply_to" not in message) and not welcomed_users[message["user"]]:
                global welcomed_users
                welcomed_users.update({message["user"]:True})
                say_hello(ws, message["user"], message["channel"])
            else:
                say_some_bullshit(ws, message["user"], message["channel"])
        elif "!help" in message["text"].lower():
            provide_help(ws, message["channel"])
        else:  # parse commands
            regex_commands = re.compile(r'!(\w*)\s(.*)')
            command = re.match(regex_commands, message["text"])
            if command:
                if command.group(1).lower() == "pogoda":  # pogoda
                    provide_weather(ws, command.group(2), message["channel"])
                else:
                    provide_help(ws, message["channel"])
            elif re.match(r'!(\w*)', message["text"]).group(1).lower() == "gra":
                if not (game_in_play or message["user"] == player):
                    global game_in_play, player
                    game_in_play = True
                    player = message["user"]
                    init_number_game(ws, users_list[message["user"]], message["channel"])
                else:
                    send_message_via_ws(ws, "message", "Zaczekaj na swoja kolejke " + users_list[message["user"]],
                                        message["channel"])

            if re.match(r'!(\w*)', message["text"]).group(1).lower() == "koniec":
                global game_in_play
                game_in_play = False
                send_message_via_ws(ws, "message", "Wymiekles " + users_list[message["user"]] + "?", message["channel"])


def on_error(ws, error):
    print error


def on_close(ws):
    print "### closed ###"


def on_open(ws):
    print "### open ###"


def get_websocket_address():
    return json.loads(requests.get(
        'https://slack.com/api/rtm.start?token=' + token).text)["url"]

def set_all_users_list():
    users_json = json.loads(requests.get('https://slack.com/api/users.list?token=' + token).text)
    global users_list, welcomed_users
    for user in users_json["members"]:
        users_list.update({user["id"]: user["profile"]["first_name"] if "first_name" in user["profile"] and
                                                                        user["profile"]["first_name"] is not None else
        user["name"]})
        welcomed_users.update({user["id"]:False})


def get_new_channels():
    channel_list = json.loads(requests.get('https://slack.com/api/channels.list?token=' + token).text)
    global all_channels
    for channel in channel_list["channels"]:
        all_channels.update({channel["id"]: channel["name"]})


def open_websocket(ws_url):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == '__main__':
    set_all_users_list()
    get_new_channels()
    open_websocket(get_websocket_address())
