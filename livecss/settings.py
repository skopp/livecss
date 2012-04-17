from .wrappers import PerFileConfig
from .wrappers import Settings


def settings_for(view):
    class wrapper: pass
    wrapper.local = local_settings(view)
    wrapper.glob = global_settings
    return wrapper

global_settings = Settings('livecss-settings.sublime-settings', False)
local_settings = lambda v: PerFileConfig(v.buffer_id(), 'LivecssState.sublime-settings', True)
