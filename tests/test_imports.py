"""
Basic tests for an application.

This ensures all modules are importable and that the config is valid.
"""

def test_import_app():
    from irrigation_gate_control.application import IrrigationGateControlApplication
    assert IrrigationGateControlApplication

def test_config():
    from irrigation_gate_control.app_config import IrrigationGateControlConfig

    assert isinstance(IrrigationGateControlConfig.to_schema(), dict)

def test_ui():
    from irrigation_gate_control.app_ui import IrrigationGateControlUI
    assert IrrigationGateControlUI

def test_tags():
    from irrigation_gate_control.app_tags import IrrigationGateControlTags
    assert IrrigationGateControlTags

def test_state():
    from irrigation_gate_control.app_state import IrrigationGateControlState
    assert IrrigationGateControlState
