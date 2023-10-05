from config import EyeTrackConfig
from osc import EyeId

from settings.BaseSettings import BaseSettingsWidget
from settings.modules.GeneralSettingsModule import GeneralSettingsModule
from settings.modules.OneEuroSettingsModule import OneEuroSettingsModule
from settings.modules.OSCSettingsModule import OSCSettingsModule


class SettingsWidget(BaseSettingsWidget):
    def __init__(self, widget_id: EyeId, main_config: EyeTrackConfig):
        settings_modules = [
            GeneralSettingsModule,
            OneEuroSettingsModule,
            OSCSettingsModule,
        ]
        super().__init__(widget_id, main_config, settings_modules)

