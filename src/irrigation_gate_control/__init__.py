from pydoover.docker import run_app

from .application import IrrigationGateControlApplication
from .app_config import IrrigationGateControlConfig

def main():
    """
    Run the application.
    """
    run_app(IrrigationGateControlApplication(config=IrrigationGateControlConfig()))
