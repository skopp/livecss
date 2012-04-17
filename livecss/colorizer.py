# -*- coding: utf-8 -*-

"""
    livecss.colorizer
    ~~~~~~~~~

    This module implements python helper objects.

"""

from .color import Color
from .fast_theme_generation import generate_theme_file
from .file_operations import rm_theme
from .helpers import escape
from .theme import theme, uncolorized_path, colorized_path

from .colors import color_regexps
from .helpers import compact, flatten


def colorize_file(view, state, forse_redraw=False):
    """Highlights color definition regions by it's real colors.
    `forse_redraw` set to True forces re-colorization

    """

    colored_regions = get_colored_regions(view)
    colors = get_colors(view, colored_regions)
    if not colors:
        return

    state.colors = colors
    state.regions = colored_regions

    if not state.is_dirty and not forse_redraw:
        return

    if forse_redraw or state.need_generate_theme_file:
        colorized_theme_path = generate_theme(uncolorized_path(theme.abspath), colors)
        if hasattr(state, 'focused') and state.focused:
            theme.set(colorized_theme_path)
        # remove previously used theme if any
        rm_theme(state.theme_path)
        # associate theme with file
        state.theme_path = colorized_theme_path

    highlight_regions(view, colored_regions, colors, state)



def uncolorize_file(view, state):
    """Removes highlighting from view,
    then delete modified theme file, set original theme.
    """

    clear_css_regions(view)
    theme.set(uncolorized_path(theme.abspath))
    rm_theme(state.theme_path)
    state.theme_path = False


# extract colors from file

def get_colors(view, color_regions):
    """Extracts text from `color_regions` and wraps it by :attr:`livecss.color.Color` object.

    :param color_regions: list of ST regions which contain color definition
    :return: list of colors wrapped by :attr:`livecss.color.Color` object

    """

    colors = [Color(view.substr(color)) for color in color_regions]
    return colors


def get_colored_regions(view):
    """Returns regions which contain color definition.

    :return: list of ST regions

    """
    return compact(flatten(view.find_all(regexp) for regexp in color_regexps))


# generate new theme file

def generate_theme(theme_path, colors):
    """Generates new ST theme file with rules for new colors.

    :param theme_path: path to ST theme file
    :param colors: list of colors wrapped by :attr:`livecss.color.Color` object
    :return: newly created theme file

    """

    colorized_theme_path = colorized_path(theme.abspath)

    new_colors = (template(color) for color in set(colors))
    generate_theme_file(theme_path, new_colors, colorized_theme_path)

    return colorized_theme_path


def template(color):
    """Template to insert in theme plist file.

    :param color: :attr:`livecss.color.Color` object
    :return: plist convert ready dict

    """

    return {
        'name': escape(color.hex),
        'scope': color.hex,
        'settings': {
            'background': color.hex,
            'foreground': color.opposite
        }
    }


# add/remove regions from view

def highlight_regions(view, regions, colors, state):
    """Highlights `regions` by `colors`

    :param regions: regions with color definition
    :param colors: colors to highlight these regions
    :param state: current state for this file. :attr:`livecss.state.State` object

    """

    regions_colors = zip(regions, colors)
    # Clear all available colored regions
    clear_css_regions(view)
    # Color regions
    count = 0
    for r, c  in regions_colors:
        name = "css_color_%d" % count
        view.add_regions(name, [r], c.hex)
        count += 1
    state.count = count


def clear_css_regions(view):
    """Removes previously highlighted regions"""

    count = 0
    while count != -1:
        name = "css_color_%d" % count
        if len(view.get_regions(name)):
            view.erase_regions(name)
            count += 1
        else:
            count = -1
