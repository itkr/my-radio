# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import functools

from modules.color import ColorString

_commands = []
_aliases = {}


def user_command(func=None, aliases=[]):
    global _commands
    global _aliases

    if func is None:
        return functools.partial(user_command, aliases=aliases)

    _commands.append(func.__name__)

    # aliase
    for alias in aliases:
        if alias in _commands:
            raise Exception('conflict')
    _commands.extend(aliases)
    _commands = list(set(_commands))
    for alias in aliases:
        _aliases[alias] = func.__name__

    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return inner


def _error(text):
    print(ColorString(text).red())


class Commands(object):

    def __init__(self, controller):
        self.controller = controller
        self._set_aliases()

    def _set_aliases(self):
        global _aliases
        for k, v in _aliases.items():
            setattr(self, k, getattr(self, v))

    @staticmethod
    def _not_fount(name, *args):
        _error('\'{}\' not found => Try \'help\''.format(name))

    @classmethod
    def get_all(cls):
        global _commands
        return _commands

    def get(self, name):
        commands = self.get_all()
        if name not in commands:
            return functools.partial(self._not_fount, name=name)
        return getattr(self, name)

    @user_command(aliases=['q'])
    def quit(self):
        self.controller.stop()

    @user_command
    def pause(self):
        self.controller.radio.play_or_stop()

    @user_command
    def help(self):
        print(self.get_all())

    @user_command
    def channels(self, area='JP13'):
        self.controller.print_channels(area)

    @user_command
    def extend(self, seconds):
        self.controller.extend(seconds)

    @user_command
    def status(self):
        self.controller.print_status()

    @user_command
    def info(self):
        self.controller.print_info()

    @user_command
    def change(self, channel_key, area='JP13'):
        self.controller.change(channel_key, area)
