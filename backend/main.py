from plugins import base_plugin
from plugins.plugins.A_SSH.backend import ssh, ui


class Plugin(base_plugin.Plugin):
    def load(self) -> bool:
        ui.fullscreen.init()
        ssh.service.init()
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
