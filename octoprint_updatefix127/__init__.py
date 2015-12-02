# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import threading

BROKEN_VERSION = "1.2.7"
FIXED_VERSION = "1.2.8"

class UpdateFix127Plugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.SettingsPlugin):

	# Note: we mark ourselves as an AssetPlugin instead of just a RestartNeedingPlugin
	# since that will also trigger our UI to show the reload dialog

	def on_after_startup(self):
		if octoprint_version_matches(BROKEN_VERSION):
			self._monkey_patch_127()
		elif octoprint_version_matches(FIXED_VERSION):
			self._uninstall_plugin()

	def _monkey_patch_127(self):
		# "octoprint.plugins.softwareupdate" is actually loaded dynamically as
		# just "softwareupdate"
		try:
			from softwareupdate import SoftwareUpdatePlugin, exceptions
		except:
			self._logger.exception("Could not import SoftwareUpdate plugin for monkey patching, aborting!")
			return

		# monkey patch the software update plugin
		self._logger.info("Monkey patching octoprint.plugins.softwareupdate.SoftwareUpdatePlugin...")
		def fixed_perform_updates(instance, check_targets=None, force=False):
			"""
			Performs the updates for the given check_targets. Will update all possible targets by default.

			:param check_targets: an iterable defining the targets to update, if not supplied defaults to all targets
			"""

			checks = instance._get_configured_checks()
			populated_checks = dict()
			for target, check in checks.items():
				try:
					populated_checks[target] = instance._populated_check(target, check)
				except exceptions.UnknownCheckType:
					instance._logger.debug("Ignoring unknown check type for target {}".format(target))
				except:
					instance._logger.exception("Error while populating check prior to update for target {}".format(target))

			if check_targets is None:
				check_targets = populated_checks.keys()
			to_be_updated = sorted(set(check_targets) & set(populated_checks.keys()))
			if "octoprint" in to_be_updated:
				to_be_updated.remove("octoprint")
				tmp = ["octoprint"] + to_be_updated
				to_be_updated = tmp

			updater_thread = threading.Thread(target=instance._update_worker, args=(populated_checks, to_be_updated, force))
			updater_thread.daemon = False
			updater_thread.start()

			return to_be_updated, dict((key, check["displayName"] if "displayName" in check else key) for key, check in populated_checks.items() if key in to_be_updated)

		SoftwareUpdatePlugin.perform_updates = fixed_perform_updates

		self._logger.info("... octoprint.plugins.softwareupdate.SoftwareUpdatePlugin monkey patched with fix for updater")
		self._logger.info("Updating to 1.2.8 should now work just fine.")

	def _uninstall_plugin(self):
		self._logger.info("Detected fixed version, uninstalling myself...")
		try:
			from pluginmanager import __plugin_implementation__ as pmgr
		except:
			self._logger.exception("Could not import Plugin Manager for uninstalling, aborting!")
			return

		if not self._identifier in self._plugin_manager.plugins:
			self._logger.error("Could not find myself in plugin manager O_O, can't uninstall myself, aborting!")
			return

		plugin = self._plugin_manager.plugins[self._identifier]

		try:
			from octoprint.server import app
		except:
			self._logger.exception("Could not import Flask app, cannot uninstall, aborting!")
			return

		with app.test_request_context("/api/plugins/plugin_manager/"):
			response = pmgr.command_uninstall(plugin)
			if response.status_code == 200:
				self._logger.info("... uninstalled myself, thanks!")
				self._perform_restart()
			else:
				self._logger.error("Error trying to uninstall myself: {!r}".format(response))

	def _perform_restart(self):
		restart_command = self._settings.global_get(["server", "commands", "serverRestartCommand"])
		if restart_command:
			self._logger.info("Restarting after uninstall of myself...")
			import sarge
			try:
				sarge.run(restart_command)
			except:
				self._logger.exception("Error while trying to restarting, please restart manually")


def octoprint_version_matches(target):
	from octoprint import __version__
	return __version__ and (__version__ == target or
	                        __version__.startswith(target + "-") or
	                        __version__.startswith(target + "."))

__plugin_name__ = "Updatefix for 1.2.7"

if not octoprint_version_matches(BROKEN_VERSION):
	__plugin_name__ += " (can be uninstalled now)"
	__plugin_description__ = "Since you are not running OctoPrint {}, this plugin is non-functional and can be uninstalled.".format(BROKEN_VERSION)

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = UpdateFix127Plugin()

