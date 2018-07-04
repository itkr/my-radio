# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import functools
import threading
import shlex
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep

from modules.channel import get_channels
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

    @user_command(aliases=['q'])
    def quit(self):
        self.controller.stop()

    @user_command
    def pause(self):
        self.controller.radio.play_or_stop()

    @user_command()
    def help(self):
        print('HELP')

    @user_command
    def channels(self, area='JP13'):
        self.controller.print_channels(area)

    @user_command
    def extend(self, seconds):
        self.controller.extend(seconds)

    @user_command
    def commands(self):
        print(_commands)

    @user_command
    def status(self):
        self.controller.print_status()

    @user_command
    def info(self):
        self.controller.print_info()

    @user_command
    def change(self, channel_key, area='JP13'):
        self.controller.change(channel_key, area)


class _PromptMixin(object):

    def _get_command(self, key):
        if not key:
            return None, None

        try:
            input_string = shlex.split(key)
            command_name = input_string[0]
            args = input_string[1:]
        except Exception as e:
            _error(e)
            return None, None

        if command_name not in _commands:
            _error('"{}" not found'.format(command_name))
            print('Try "commands"')
            return None, None

        try:
            command = getattr(Commands(self), command_name)
        except AttributeError as e:
            _error(e)
            return None, None

        return command, args

    def _do_command(self, key):
        (command, args) = self._get_command(key)
        if not command:
            return
        try:
            return command(*args)
        except Exception as e:
            _error(e)

    def _prompt(self):
        try:
            user_input = raw_input
        except NameError:
            user_input = input

        prompt_title = ColorString('radio> ').purple()
        while not self._stop:
            try:
                user_in = user_input(prompt_title)
                self._do_command(user_in)
            except EOFError:
                self.stop()


class Controller(_PromptMixin):
    _stop = False

    def __init__(self, radio, timer=0):
        self.radio = radio
        self.start_time = datetime.now()
        self.end_time = None
        if timer:
            self.end_time = self.start_time + timedelta(seconds=timer)

        self.print_status()
        self.print_info()

        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _check_time(self):
        if not self.end_time:
            return
        if self.end_time < datetime.now():
            self.stop()

    def _loop(self):
        while not self._stop:
            sleep(1)
            self._check_time()

    def start(self):
        self._loop()

    def stop(self):
        self._stop = True
        print('Good bye.')

    def extend(self, seconds):
        seconds = int(seconds)
        if not self.end_time:
            self.end_time = datetime.now()
        self.end_time += timedelta(seconds=int(seconds))
        self.print_status()

    def change(self, channel_key, area='JP13'):
        channel = get_channels(area).get(channel_key)
        if not channel:
            _error('{} not found'.format(channel_key))
            return
        self.radio.reload(channel['url'])
        self.print_info()

    def print_channels(self, area='JP13'):
        pprint(get_channels(area))

    def print_info(self):
        for key, value in self.radio.get_info().items():
            title = ColorString(key.capitalize()).yellow().under_line()
            print('{}:\n{}'.format(title, value))

    def print_status(self):
        status = {
            'start': self.start_time.isoformat(),
            'end': self.end_time.isoformat() if self.end_time else '',
        }
        for key, value in status.items():
            print('{}: \n{}'.format(ColorString(
                key.capitalize()).yellow().under_line(), value))
