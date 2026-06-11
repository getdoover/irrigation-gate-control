from pydoover.docker import run_app

from .application import IrrigationGateControlApplication


def main():
    """
    Run the application.
    """
    run_app(IrrigationGateControlApplication())
