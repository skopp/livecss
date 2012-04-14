# -*- coding: utf-8 -*-

"""
    livecolors
    ~~~~~~~~~

    ST commands.

"""

import sublime_plugin

# local imports
from livecss.colorizer import colorize_file, uncolorize_file
from livecss.file_operations import clean_junk
from livecss.state import state_for
from livecss.theme import theme
from livecss.utils import (need_colorization, need_uncolorization, generate_default_settings,
                           is_colorizable, generate_menu, colorize_on_select_new_theme)
from livecss.settings import settings_for, toggle


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
        state.focused = True
        if state and state.theme_path:
            # set file's own theme path, because we use one per file
            theme.set(state.theme_path)

        if need_colorization(view):
            colorize_file(view, state, True)

        if need_uncolorization(view):
            uncolorize_file(view, state_for(view))


class ToggleLocalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        settings = settings_for(view)
        if settings.local.autocolorize:
            uncolorize_file(view, state)
        else:
            colorize_file(view, state, True)
        toggle(settings.local, 'autocolorize')
        generate_menu(view)

    def is_visible(self):
        return is_colorizable(self.view)


class ToggleGlobalLiveCssCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        state = state_for(view)
        settings = settings_for(view)
        if settings.glob.autocolorize and settings.local.autocolorize:
            uncolorize_file(view, state)
        elif not settings.glob.autocolorize and settings.local.autocolorize in ['undefined', False]:
            colorize_file(view, state, True)
        toggle(settings.glob, 'autocolorize')
        generate_menu(view)

    def is_visible(self):
        return is_colorizable(self.view)
