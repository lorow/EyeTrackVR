from typing import Callable

import PySimpleGUI as sg

from config import EyeTrackConfig
from EyeTrackApp.consts import PageType

from settings.constants import BACKGROUND_COLOR
from settings.modules.general_settings_module import GeneralSettingsModule
from settings.modules.keyboard_shortcuts_module import KeyboardShortcutsModule
from settings.modules.osc_module import OSCSettingsModule
from settings.modules.tracking_algorithm_module import TrackingAlgorithmsModule


# TODO there used to be validation problems here, try to find them and fix them
class SettingsWidget:
    def __init__(
        self,
        widget_id: PageType,
        main_config: EyeTrackConfig,
    ):
        self.gui_status = "-STATUS-"
        self.gui_general_settings_layout = f"-GENERALSETTINGSLAYOUT{widget_id}-"

        self.main_config = main_config
        self.config = main_config.settings

        self.validation_errors = []

        settings_modules: Callable = [
            GeneralSettingsModule,
            # TrackingAlgorithmsModule,
            KeyboardShortcutsModule,
            OSCSettingsModule,
        ]
        self.initialized_modules = self._initialize_modules(settings_modules, widget_id=widget_id)

        self.settings_layout = []

        for module in self.initialized_modules:
            self.settings_layout.extend(
                module.get_layout()
            )

        self.widget_layout = [
            [
                sg.StatusBar(
                    self.validation_errors,
                    size=(1, 1),
                    key=self.gui_status,
                    background_color=BACKGROUND_COLOR,
                )
            ],
            [
                sg.Column(
                    self.settings_layout,
                    key=self.gui_general_settings_layout,
                    background_color=BACKGROUND_COLOR,
                ),
            ],
        ]

    def _initialize_modules(self, modules, widget_id):
        initialized_modules = []
        for module in modules:
            initialized_modules.append(
                module(settings=self.main_config, config=self.config, widget_id=widget_id)
            )
        return initialized_modules

    def render(self, window, event, values):
        validated_data, errors = {}, []
        for module in self.initialized_modules:
            module_validated_data, module_errors = module.validate(values)
            if module_validated_data:
                validated_data.update(module_validated_data)
            if errors:
                errors.extend(module_errors)

        if not errors and validated_data:
            self.main_config.update(validated_data)
            self.main_config.save()


        # if self.config.gui_min_cutoff != values[self.gui_min_cutoff]:
        #     self.config.gui_min_cutoff = values[self.gui_min_cutoff]
        #     changed = True
        #
        # if self.config.gui_speed_coefficient != values[self.gui_speed_coefficient]:
        #     self.config.gui_speed_coefficient = values[self.gui_speed_coefficient]
        #     changed = True
        #
        # if self.config.gui_HSFP != int(values[self.gui_HSFP]):
        #     self.config.gui_HSFP = int(values[self.gui_HSFP])
        #     changed = True
        #
        # if self.config.gui_HSF != values[self.gui_HSF]:
        #     self.config.gui_HSF = values[self.gui_HSF]
        #     changed = True
        #
        # if self.config.gui_DADDYP != int(values[self.gui_DADDYP]):
        #     self.config.gui_DADDYP = int(values[self.gui_DADDYP])
        #     changed = True
        #
        # if self.config.gui_DADDY != values[self.gui_DADDY]:
        #     self.config.gui_DADDY = values[self.gui_DADDY]
        #     changed = True
        #
        # if self.config.gui_RANSAC3DP != int(
        #     values[self.gui_RANSAC3DP]
        # ):  # TODO check that priority order is unique/auto fix it.
        #     self.config.gui_RANSAC3DP = int(values[self.gui_RANSAC3DP])
        #     changed = True
        #
        # if self.config.gui_RANSAC3D != values[self.gui_RANSAC3D]:
        #     self.config.gui_RANSAC3D = values[self.gui_RANSAC3D]
        #     changed = True
        #
        # if self.config.gui_HSRACP != int(values[self.gui_HSRACP]):
        #     self.config.gui_HSRACP = int(values[self.gui_HSRACP])
        #     changed = True
        #
        # if self.config.gui_HSRAC != values[self.gui_HSRAC]:
        #     self.config.gui_HSRAC = values[self.gui_HSRAC]
        #     changed = True
        #
        # if self.config.gui_skip_autoradius != values[self.gui_skip_autoradius]:
        #     self.config.gui_skip_autoradius = values[self.gui_skip_autoradius]
        #     changed = True
        #
        # if self.config.gui_BLINK != values[self.gui_BLINK]:
        #     self.config.gui_BLINK = values[self.gui_BLINK]
        #     changed = True
        #
        # if self.config.gui_IBO != values[self.gui_IBO]:
        #     self.config.gui_IBO = values[self.gui_IBO]
        #     changed = True
        #
        # if self.config.gui_circular_crop_left != values[self.gui_circular_crop_left]:
        #     self.config.gui_circular_crop_left = values[self.gui_circular_crop_left]
        #     changed = True
        #
        # if self.config.gui_circular_crop_right != values[self.gui_circular_crop_right]:
        #     self.gui_circular_crop_right = values[self.gui_circular_crop_right]
        #     changed = True
        #
        # if self.config.gui_HSF_radius != int(values[self.gui_HSF_radius]):
        #     self.config.gui_HSF_radius = int(values[self.gui_HSF_radius])
        #     changed = True
        #
        # if self.config.gui_BLOB != values[self.gui_BLOB]:
        #     self.config.gui_BLOB = values[self.gui_BLOB]
        #     changed = True
        #
        # if self.config.gui_BLOBP != int(values[self.gui_BLOBP]):
        #     self.config.gui_BLOBP = int(values[self.gui_BLOBP])
        #     changed = True
        #
        # if self.config.gui_threshold != values[self.gui_threshold_slider]:
        #     self.config.gui_threshold = int(values[self.gui_threshold_slider])
        #     changed = True
        #
        # if self.config.gui_thresh_add != values[self.gui_thresh_add]:
        #     self.config.gui_thresh_add = int(values[self.gui_thresh_add])
        #     changed = True
        #
        # if self.config.gui_eye_falloff != values[self.gui_eye_falloff]:
        #     self.config.gui_eye_falloff = values[self.gui_eye_falloff]
        #     changed = True
        #
        # if self.config.gui_blob_maxsize != values[self.gui_blob_maxsize]:
        #     self.config.gui_blob_maxsize = values[self.gui_blob_maxsize]
        #     changed = True
