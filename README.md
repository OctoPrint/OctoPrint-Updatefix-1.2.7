# OctoPrint Updatefix 1.2.7

This plugin fixes an issue in OctoPrint 1.2.7's software updater, causing updates
of OctoPrint itself to fail.

The plugin monkey-patches the bug causing this issue, but only for affected versions.
Once version 1.2.8 (which ships with a fix) is detected, the plugin uninstalls
itself during startup utilizing the plugin manager.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-Updatefix-1.2.7/archive/master.zip

