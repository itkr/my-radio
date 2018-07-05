# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function, unicode_literals


class ColorString(str):

    _colors = {
        'red': '\033[91m',
        'yellow': '\033[93m',
        'purple': '\033[95m',
    }

    _decorations = {
        'under_line': '\033[4m',
    }

    def __init__(self, s='', *args, **kwargs):
        self._string = str(s)
        self._color = ''
        self._decoration = ''
        super(ColorString, self).__init__()

    def __str__(self):
        return self._make()

    def __repr__(self):
        return self._make()

    def _make(self):
        return ''.join(
            [self._decoration, self._color, self._string, '\033[0m'])

    def _set_decoration(self, decoration):
        self._decoration = self._decorations.get(decoration, '')
        return self

    def _set_color(self, color):
        self._color = self._colors.get(color, '')
        return self

    def purple(self):
        return self._set_color('purple')

    def yellow(self):
        return self._set_color('yellow')

    def red(self):
        return self._set_color('red')

    def under_line(self):
        return self._set_decoration('under_line')


def print_error(text):
    print(ColorString(text).red())
