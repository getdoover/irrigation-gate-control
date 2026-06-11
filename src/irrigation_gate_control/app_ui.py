from pathlib import Path

from pydoover import ui


class IrrigationGateControlUI(ui.UI, default_open=True):
    open_now = ui.Button(
        "Open Now",
        position=1,
        colour=ui.Colour.green,
        requires_confirm=True,
    )
    close_now = ui.Button(
        "Close Now",
        position=2,
        colour=ui.Colour.green,
        requires_confirm=True,
    )


def export():
    IrrigationGateControlUI(None, None, None).export(
        Path(__file__).parents[2] / "doover_config.json",
        "irrigation_gate_control",
    )
