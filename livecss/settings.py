from .wrappers import PerFileConfig
from .wrappers import Settings

settings = Settings('LiveCSS.sublime-settings', False)


class LocalSettings(PerFileConfig):
    """Object which wraps ST settings entity.
    Properties started with `global_` are global setting.
    Properties started with `local_` are unique for file.
    Default value is True.

    """

    def __init__(self, view):
        super(LocalSettings, self).__init__(view.buffer_id(), 'LivecssState.sublime-settings', in_memory=False)
