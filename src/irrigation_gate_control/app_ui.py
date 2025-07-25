from pydoover import ui

def get_remote_key(remote):
    return remote.lower().replace(" ", "_")

class IrrigationGateControlUI:
    def __init__(self, app):
        self.app = app

        self.open_now = ui.Action(
            "open_now",
            "Open Now",
            position=1,
            colour=ui.Colour.green,
            requires_confirm=True,
        )
        self.close_now = ui.Action(
            "close_now",
            "Close Now",
            position=2,
            colour=ui.Colour.green,
            requires_confirm=True,
        )
        self.stop_now = ui.Action(
            "stop_now",
            "Stop Now",
            position=3,
            colour=ui.Colour.red,
            requires_confirm=False,
        )

    def fetch(self):
        return self.open_now, self.close_now, self.stop_now

    def update(self):
        pass
