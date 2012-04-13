# -*- coding: utf-8 -*-

"""
    livecolors
    ~~~~~~~~~

    ST commands.

"""

import sublime_plugin

# local imports
from livecss.colorizer import colorize_file, uncolorize_file
from livecss.file_operatios import clean_junk
from livecss.state import state_for
from livecss.theme import theme
from livecss.utils import (need_colorization, need_uncolorization, generate_default_settings,
                           is_colorizable, generate_menu, colorize_on_select_new_theme)
from livecss.settings import LocalSettings, settings


class CssColorizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        colorize_file(self.view, state_for(self.view), True)


class CssUncolorizeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        uncolorize_file(self.view, state_for(self.view))


class EventManager(sublime_plugin.EventListener):
    def __init__(self):
        # before anything
        clean_junk()
        generate_default_settings()

    def on_load(self, view):
        # set hook to recolorize if different theme was chosen
        theme.on_select_new_theme(lambda: colorize_on_select_new_theme(view))

        if need_colorization(view):
            colorize_file(view, state_for(view))

    def on_close(self, view):
        if need_uncolorization(view):
            uncolorize_file(view, state_for(view))

    def on_modified(self, view):
        if need_colorization(view):
            colorize_file(view, state_for(view))

    def on_activated(self, view):
        if is_colorizable(view):
            generate_menu(view)

        state = state_for(view)
        if state and state.theme_path:
            # set file's own theme path, because we use one per css file
            theme.set(state.theme_path)

        if need_colorization(view):
            colorize_file(view, state, True)

        if need_uncolorization(view):
            uncolorize_file(view, state_for(view))


class ToggleLocalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        autocolorize_locally = LocalSettings(view).local_on
        if autocolorize_locally:
            uncolorize_file(view, state)
        else:
            colorize_file(view, state, True)
        LocalSettings(view).local_on = not LocalSettings(view).local_on
        generate_menu(view)

    def is_visible(self):
        return is_colorizable(self.view)


class ToggleGlobalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        autocolorize_locally = LocalSettings(view).local_on
        autocolorize_globally = settings['autocolorization']
        if autocolorize_globally and autocolorize_locally:
            uncolorize_file(view, state)
        elif not autocolorize_globally and autocolorize_locally in ['undefined', False]:
            colorize_file(view, state, True)

        settings['autocolorization'] = not settings['autocolorization']
        generate_menu(view)

    def is_visible(self):
        return is_colorizable(self.view)
