"""Resource settings — disposition adapts to what exists around the
doctor; the level of concern never does (Stage 8 Task 8.2)."""
from .disposition import (
    SETTINGS,
    DEFAULT_SETTING,
    available_settings,
    describe_setting,
    disposition_guidance,
    setting_line,
)

__all__ = [
    "SETTINGS",
    "DEFAULT_SETTING",
    "available_settings",
    "describe_setting",
    "disposition_guidance",
    "setting_line",
]
