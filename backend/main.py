from plugins import base_plugin
from plugins.plugins.A_SSH.backend.ui import fullscreen
from plugins.plugins.A_SSH.backend.ssh import service


class Plugin(base_plugin.Plugin):
    def load(self) -> bool:
        fullscreen.init()
        service.init()
        return True

    def unload(self) -> bool:
        return True

    def health(self) -> bool:
        return True

    def image(self) -> str:
        return 'sample.svg'

    @property
    def name(self) -> str:
        return 'A-SSH'


def init() -> Plugin:
    return Plugin()
