# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import threading
import shlex

from modules.color import ColorString, print_error

from .base import BaseController

# python3: input, python2: raw_input
try:
    _input = raw_input
except NameError:
    _input = input


class PromptController(BaseController):

    def __init__(self, radio, timer=0):
        super(PromptController, self).__init__(radio, timer)
        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _execute(self, user_input):
        try:
            inputs = shlex.split(user_input)
            if self._stop:
                return
            command = self.commands.get(inputs[0])
            return command(*inputs[1:])
        except Exception as e:
            print_error(e)

    def _prompt(self):
        try:
            while not self._stop:
                user_input = _input(ColorString('radio> ').purple())
                if user_input:
                    self._execute(user_input)
        except EOFError:
            self.stop()
