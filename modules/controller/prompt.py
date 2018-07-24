# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals

import shlex
import threading

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import ANSI

from modules.color import ColorString, print_error

from .base import BaseController


class PromptController(BaseController):

    def __init__(self, radio, timer=0):
        super(PromptController, self).__init__(radio, timer)
        self.prompt = threading.Thread(target=self._prompt)
        self.prompt.start()

    def _execute(self, user_input):
        try:
            inputs = shlex.split(user_input)
            command = self.commands.get(inputs[0])
            return command(*inputs[1:])
        except Exception as e:
            print_error(e)

    def _prompt(self):
        commands = self.commands.get_all()
        reserved_words_completer = WordCompleter(commands)
        try:
            while not self._stop:
                user_input = prompt(ANSI('\x1b[35mradio> '),
                                    completer=reserved_words_completer)
                if user_input and not self._stop:
                    self._execute(user_input)
        except EOFError:
            self.stop()
        except KeyboardInterrupt:
            self.stop()
        except ValueError:
            pass
