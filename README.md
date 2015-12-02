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

## How does it work?

After installing the plugin and restarting, the plugin will check if you are
running OctoPrint version 1.2.7 or 1.2.8.

If you are running 1.2.7, it will apply a patch to the loaded class of the Software
Update Plugin (so called monkey patching) during start up of the server, effectively
applying the same fix for the bug that prevents updating to 1.2.8 from working
that is also present in 1.2.8. Once your server has started you may then update
as usual.

Once the plugin detects version 1.2.8 as running, it will uninstall itself
and restarting the server.

Usually the process will look like the following:

1. You are running 1.2.7.
2. You install the plugin and are prompted to restart the server.
3. You restart.
4. You perform the update to 1.2.8. The server is restarted.
5. The plugin detects you are now running 1.2.8. It uninstalls itself and
   restarts the server.
6. You have a clean 1.2.8 install.
