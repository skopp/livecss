# -*- coding: utf-8 -*-

"""
    livecss.colorizer
    ~~~~~~~~~

    This module implements some useful utilities.

"""
import os

import sublime

# local imports

from .state import state_for
from .theme import theme, uncolorized_path
from .colorizer import colorize_file
from .menu import create_menu
from .settings import settings_for


def colorize_on_select_new_theme(view):
    state = state_for(view)
    if not state.theme_path:
        return
    if uncolorized_path(state.theme_path) != uncolorized_path(theme.abspath):
        # here is small hack to colorize after we change the theme
        # TODO: find out better solution
        sublime.set_timeout(lambda: colorize_file(view, state, True), 200)


def generate_menu(view):
    s = settings_for(view)
    create_menu(s.local.autocolorize, s.glob.autocolorize)


def file_id(view):
    return view.file_name() or view.buffer_id()


def is_colorizable(view):
    s = settings_for(view)
    point = view.sel()[0].begin()
    file_scope = view.scope_name(point).split()[0]
    file_name = view.file_name()
    if file_name:
        file_ext = file_name.split('.')[-1]
    else:
        file_ext = ""
    if file_scope in s.glob.colorized_formats or file_ext in s.glob.colorized_formats:
        return True


def need_colorization(view):
    if not is_colorizable(view):
        return
    s = settings_for(view)
    if s.glob.autocolorize and s.local.autocolorize in ['undefined', True]:
        return True
    if not s.local.autocolorize:
        return False


def need_uncolorization(view):
    if not is_colorizable(view):
        return
    s = settings_for(view)
    if not s.glob.autocolorize and s.local.autocolorize is 'undefined':
        return True
    if s.local.autocolorize:
        return False


def generate_default_settings():
    if not os.path.exists(os.path.join(sublime.packages_path(), 'User', 'livecss-settings.sublime-settings')):
        s = settings_for(False)
        s.glob.colorized_formats = ["source.css", "source.css.less", "source.sass"]
        s.glob.autocolorize = True
