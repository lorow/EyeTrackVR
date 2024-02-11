from queue import Queue

from config import EyeTrackConfig
from eye import EyeId
from osc.OSCMessage import OSCMessage, OSCMessageType
from settings.BaseSettings import BaseSettingsWidget


class VRCFTSettingsWidget(BaseSettingsWidget):
    def __init__(self, widget_id: EyeId, main_config: EyeTrackConfig, osc_queue_in: Queue[OSCMessage]):
        self.osc_queue = osc_queue_in

        settings_modules = []
        super().__init__(widget_id, main_config, settings_modules)

    def _update_and_save_config(self, validated_data: dict):
        self.main_config.update(validated_data, save=True)

        for field, value in validated_data.items():
            self.osc_queue.put(
                OSCMessage(
                    type=OSCMessageType.VRCFT_MODULE_INFO,
                    data={
                        "command": "set",
                        "field": field,
                        "value": value,
                    },
                )
            )

        self.is_saving = False

    def reset_config(self, window):
        """resets the module for both, the ETVR app and the module"""
        super().reset_config(window=window)
        self.osc_queue.put(
            OSCMessage(
                type=OSCMessageType.VRCFT_MODULE_INFO,
                data={"command": "reset"},
            )
        )
