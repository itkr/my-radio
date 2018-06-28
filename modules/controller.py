# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import threading
from datetime import datetime, timedelta
from time import sleep

_commands = []


def user_command(func):
    _commands.append(func.__name__)

    def inner(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return inner


class _UserCommandMixin(object):

    @user_command
    def q(self):
        self.stop()

    @user_command
    def pause(self):
        self.radio.play_or_stop()

    @user_command
    def help(self):
        print('HELP')

    @user_command
    def channels(self):
        print('CHANNELS')

    @user_command
    def extend(self, seconds):
        print('EXTEND', seconds)

    @user_command
    def commands(self):
        print(_commands)


class Controller(_UserCommandMixin):
    _stop = False

    def __init__(self, radio, playback=60):
        self.radio = radio
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=playback)
        print('Start: {}'.format(self.start_time.isoformat()))
        print('End: {}'.format(self.end_time.isoformat()))

        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _get_command(self, key):
        if not key:
            return
        try:
            command_name = key.split('(')[0]
        except Exception:
            print(e)
            return
        if command_name not in _commands:
            print('"{}" not found'.format(command_name))
            return
        return 'self.{}'.format(key)

    def _do_command(self, key):
        command = self._get_command(key)
        if not command:
            return
        try:
            return eval(command)
        except Exception as e:
            print(e)

    def _prompt(self):
        while not self._stop:
            try:
                user_in = raw_input('radio> ')
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
