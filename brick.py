# -*- coding: utf-8 -*-
__author__ = 'Andrzej'
import re

def replace_channels_links(match):
    match = match.group()
    return match
users_list = {'U0CMB1KFZ':'wiktorinoxina'}

s = r' <@U0CMB1KFZ|wiktoria> has joined the channel'
pattern = re.compile(r'<@(\S{0,})>')

def replace_channels_links(match):
    match = match.group()
    if '|' in match:
        return match[match.index('|') + 1:-1]
    return users_list[match[2:11]]

s = re.sub(pattern,replace_channels_links,s)

print s