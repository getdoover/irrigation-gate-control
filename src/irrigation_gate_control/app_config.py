from pathlib import Path

from pydoover import config
from pydoover.config import ApplicationPosition, ApplicationDefaultOpen


class IrrigationGateControlConfig(config.Schema):
    hydraulic_controller = config.Application(
        "Hydraulic Controller",
        description="The application which controls the hydraulic system",
        default=None,
    )
    controlled_remote = config.String(
        "Controlled Remote",
        description="The name of the remote which controls the gate",
        default=None,
    )
    open_direction = config.Enum(
        "Open Direction",
        description="The direction of oil flow that causes the gate to open. The other direction will cause the gate to close.",
        choices=["Forward", "Reverse"],
        default="Forward",
    )
    open_timeout = config.Integer(
        "Open Timeout",
        description="The number of seconds that the remote will be running to open the gate",
        default=5,
    )
    close_timeout = config.Integer(
        "Close Timeout",
        description="The number of seconds that the remote will be running to close the gate",
        default=5,
    )

    position = ApplicationPosition()
    default_open = ApplicationDefaultOpen()


def export():
    IrrigationGateControlConfig.export(
        Path(__file__).parents[2] / "doover_config.json",
        "irrigation_gate_control",
    )
