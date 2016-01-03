# -*- coding: utf-8 -*-
__author__ = 'Andrzej'

# try:
import simplejson as json
# except ImportError:
# import json
import sys, requests, collections, datetime, re
from PyQt4 import QtCore, QtGui
from slack import Ui_MainWindow

token = ''
channel_dictionary = collections.OrderedDict()
all_channels = {}
current_channel_index = ''
users_list = {}
debug = False


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(464, 428)
        self.set_user_channel_list()
        self.set_all_users_list()
        self.assignWidgets()
        self.combo_changed()
        self.postButton.setFocus()
        self.show()

    # set channel_dictionary with channel list user is_member
    def set_user_channel_list(self):
        channel_json = json.loads(requests.get('https://slack.com/api/channels.list?token=' + token).text)
        global channel_dictionary
        for channels in channel_json["channels"]:
            all_channels.update({channels["id"]: channels["name"]})
            if channels["is_member"]:
                channel_dictionary.update({channels["id"]: channels["name"]})

    # convert unix ts to date
    def convert_slack_ts_to_date(self, ts):
        return datetime.datetime.fromtimestamp(float(ts[:-7])).strftime('%Y-%m-%d %H:%M:%S')

    # get list of the channel names from channel_dictionary
    def get_channels_list(self):
        return channel_dictionary.values()

    # get channel index we can use for json query
    def get_channel_index_from_name(self, channel_name):
        return next((index for index, name in channel_dictionary.items() if name == channel_name), None)

    # get channel historical messages
    def get_channel_historical_messages(self):
        return json.loads(requests.get(
            'https://slack.com/api/channels.history?token=' + token + '&channel=' + current_channel_index).text)

    # replace channel links
    def replace_channels_links(self, match):
        match = match.group()
        return "#" + all_channels[match[2:-1]]

    def replace_users_links(self, match):
        match = match.group()
        if '|' in match:
            return match[match.index('|') + 1:-1]
        return users_list[match[2:11]]

    def parse_channel_historical_messages(self, api_response):

        output = ""
        for message in api_response["messages"][::-1]:
            if "subtype" in message and message["subtype"] == "bot_message":
                output = output + self.convert_slack_ts_to_date(message["ts"]) + " : " + message[
                    "username"] + " (BOT) \n " + message["text"] + "\n\n"
            else:
                output = output + self.convert_slack_ts_to_date(message["ts"]) + " : " + self.get_user_name_for_id(
                    message["user"]) + "\n " + message["text"] + "\n\n"
        # parse for user names
        start = datetime.datetime.now()
        regex_users = re.compile(r'<@(\S{0,})>')
        output = re.sub(regex_users, self.replace_users_links, output)
        # parse for channels
        regex_channels = re.compile(r'<#(\S{0,})>')
        output = re.sub(regex_channels, self.replace_channels_links, output)
        end = datetime.datetime.now()
        if debug:
            print ('regex time: ' + str(end - start))

        return output

    # TODO:should scroll to end
    def reload_channel_history(self):
        start = datetime.datetime.now()
        self.channelHistoryTextEdit.setPlainText(
            self.parse_channel_historical_messages(self.get_channel_historical_messages()))
        self.channelHistoryTextEdit.moveCursor(QtGui.QTextCursor.End)
        end = datetime.datetime.now()
        if debug:
            print ('reload_channel_history time: ' + str(end - start))

    # button click signal - will post test to currently selected channel, need to remove #,&,?
    def send_post(self):
        if len(self.messageEditField.text()):
            text = str(self.messageEditField.text())
            r = requests.post(
                'https://slack.com/api/chat.postMessage?token=' + token + '&channel=' + current_channel_index + '&text=' + text.translate(
                    None, "#&?") + '&username=ajasonek&parse=full&pretty=1&as_user=true')
            if r.status_code == 200:
                self.messageEditField.clear()
                self.reload_channel_history()

    def set_all_users_list(self):
        users_json = json.loads(requests.get('https://slack.com/api/users.list?token=' + token).text)
        global users_list
        for user in users_json["members"]:
            users_list.update({user["id"]: user["real_name"]})

    def get_user_name_for_id(self, id):
        return users_list[id]

    def assignWidgets(self):
        self.postButton.clicked.connect(self.send_post)
        self.comboChannel.clear()
        self.comboChannel.addItems(self.get_channels_list())
        self.comboChannel.currentIndexChanged.connect(self.combo_changed)
        self.channelHistoryTextEdit.setReadOnly(True)

    def combo_changed(self):
        global current_channel_index
        current_channel_index = self.get_channel_index_from_name(self.comboChannel.currentText())
        self.reload_channel_history()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
