# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import functools
import threading
import shlex
from datetime import datetime, timedelta
from time import sleep

_commands = []


def user_command(func=None, aliases=[]):

    if func is None:
        return functools.partial(user_command, aliases=aliases)

    global _commands
    _commands.append(func.__name__)
    for alias in aliases:
        if alias in _commands:
            print(alias, _commands)
            raise Exception('conflict')
    _commands.extend(aliases)
    _commands = list(set(_commands))

    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)

    return inner


class _UserCommandMixin(object):

    @user_command(aliases=['q'])
    def quit(self):
        self.stop()

    @user_command
    def pause(self):
        self.radio.play_or_stop()

    @user_command()
    def help(self):
        print('HELP')

    @user_command
    def channels(self):
        print('CHANNELS')

    @user_command
    def extend(self, seconds):
        seconds = int(seconds)
        self.end_time = self.end_time + timedelta(seconds=seconds)
        self.print_status()

    @user_command
    def commands(self):
        print(_commands)

    @user_command
    def status(self):
        self.print_status()


class Controller(_UserCommandMixin):
    _stop = False

    def __init__(self, radio, playback=60):
        self.radio = radio
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=playback)
        self.print_status()
        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _get_command(self, key):
        if not key:
            return None, None
        try:
            input_string = shlex.split(key)
            command_name = input_string[0]
            args = input_string[1:]
        except Exception as e:
            print(e)
            return None, None
        if command_name not in _commands:
            print('"{}" not found'.format(command_name))
            return None, None
        return getattr(self, command_name), args

    def _do_command(self, key):
        (command, args) = self._get_command(key)
        if not command:
            return
        try:
            return command(*args)
        except Exception as e:
            print(e)

    def _prompt(self):
        try:
            user_input = raw_input
        except NameError:
            user_input = input

        while not self._stop:
            try:
                user_in = user_input('radio> ')
            except EOFError:
                self.stop()
                break
            self._do_command(user_in)

    def _start_loop(self):
        while not self._stop:
            sleep(1)
            if self.end_time < datetime.now():
                self.stop()

    def start(self):
        self._start_loop()

    def stop(self):
        self._stop = True

    def print_status(self):
        print('Start: {}'.format(self.start_time.isoformat()))
        print('End: {}'.format(self.end_time.isoformat()))
