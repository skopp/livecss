import sublime

from .wrappers import PerFileConfig
from .wrappers import Settings


def settings_for(view):
    class wrapper:
        pass
    if view.__class__ == sublime.View:
        wrapper.local = PerFileConfig(view.buffer_id(), 'LivecssState.sublime-settings', True)
    wrapper.glob = Settings('LiveCSS.sublime-settings', False)
    return wrapper


def toggle(obj, key):
    setattr(obj, key, not getattr(obj, key))
