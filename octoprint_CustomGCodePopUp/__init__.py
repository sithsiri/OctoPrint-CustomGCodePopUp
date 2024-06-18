# coding=utf-8

import octoprint.plugin
import re

class CustomGCodePopUp(octoprint.plugin.AssetPlugin,
				octoprint.plugin.TemplatePlugin,
				octoprint.plugin.SettingsPlugin):

	def SentGCodeAlert(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if len(self._settings.get(["regex_include"])) > 0 and gcode:
			popup_message = cmd
			if re.search(self._settings.get(["regex_include"]), popup_message) is None:
				return
			else:
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=popup_message))
				return
		return
	
	def ReceivedGCodeAlert(self, comm_instance, line, *args, **kwargs):
		if len(self._settings.get(["regex_include"])) > 0:
			popup_message = line
			if re.search(self._settings.get(["regex_include"]), popup_message) is not None:
				self._plugin_manager.send_plugin_message(self._identifier, dict(type="popup", msg=popup_message))
				return line
		
		return line


	##-- AssetPlugin hooks
	def get_assets(self):
		return dict(js=["js/CustomGCodePopUp.js"])

	##-- Settings hooks
	def get_settings_defaults(self):
		return dict(msgType="info",autoClose=True,enableSpeech=False,speechVoice="",speechVolume=1,speechPitch=1,speechRate=1,regex_include="")

	##-- Template hooks
	def get_template_configs(self):
		return [dict(type="settings",custom_bindings=True)]

	##~~ Softwareupdate hook
	def get_version(self):
		return self._plugin_version

	def get_update_information(self):
		return dict(
			customgcodepopup=dict(
				displayName="CustomGCodePopUp",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="sithsiri",
				repo="OctoPrint-CustomGCodePopUp",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/sithsiri/OctoPrint-CustomGCodePopUp/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "CustomGCodePopUp"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CustomGCodePopUp()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.sent": __plugin_implementation__.SentGCodeAlert,
		"octoprint.comm.protocol.gcode.received": __plugin_implementation__.ReceivedGCodeAlert,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}