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
from .settings import LocalSettings, settings


def colorize_on_select_new_theme(view):
    state = state_for(view)
    if not state.theme_path:
        return
    if uncolorized_path(state.theme_path) != uncolorized_path(theme.abspath):
        # here is small hack to colorize after we change the theme
        # TODO: find out better solution
        sublime.set_timeout(lambda: colorize_file(view, state, True), 200)


def generate_menu(view):
    autocolorize_locally = LocalSettings(view).local_on
    autocolorize_globally = settings['autocolorization']
    create_menu(autocolorize_locally, autocolorize_globally)


def file_id(view):
    return view.file_name() or view.buffer_id()


def is_colorizable(view):
    point = view.sel()[0].begin()
    file_scope = view.scope_name(point).split()[0]
    file_name = view.file_name()
    if file_name:
        file_ext = file_name.split('.')[-1]
    else:
        file_ext = ""
    # if not file_scope is 'source.python':
    #     return True
    if file_scope in settings['colorized_formats'] or file_ext in settings['colorized_formats']:
        return True


def need_colorization(view):
    if not is_colorizable(view):
        return

    autocolorize_locally = LocalSettings(view).local_on
    autocolorize_globally = settings['autocolorization']

    if autocolorize_globally and autocolorize_locally in ['undefined', True]:
        return True

    if not autocolorize_locally:
        return False


def need_uncolorization(view):
    if not is_colorizable(view):
        return

    autocolorize_locally = LocalSettings(view).local_on
    autocolorize_globally = settings['autocolorization']

    if not autocolorize_globally and autocolorize_locally is 'undefined':
        return True

    if autocolorize_locally:
        return False


def generate_default_settings():
    if not os.path.exists(os.path.join(sublime.packages_path(), 'User', 'LiveCSS.sublime-settings')):
        settings['colorized_formats'] = ["source.css", "source.css.less", "source.sass"]
        settings['autocolorization'] = True
