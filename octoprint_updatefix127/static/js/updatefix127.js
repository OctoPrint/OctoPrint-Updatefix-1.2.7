$(function() {
    function Updatefix127ViewModel() {
        var self = this;

        self.infodialog = undefined;

        self.onStartup = function() {
            self.infodialog = $("#plugin_updatefix127_infodialog");
            self.infodialog.on("hidden", function() {
                self._showNotification();
            });
        };

        self.onDataUpdaterReconnect = function() {
            if (self._isBrokenVersion(VERSION)) {
                self._showDialog();
            }
        };

        self.onStartupComplete = function() {
            // run once after startup is complete
            self.onDataUpdaterReconnect();
        };

        self._isBrokenVersion = function(version) {
            return self._isVersion(version, "1.2.7");
        };

        self._isVersion = function(version, test) {
            return version == test || _.startsWith(version, test + ".") || _.startsWith(version, test + "-");
        };

        self._showDialog = function() {
            if (self.infodialog.length) {
                self.infodialog.modal("show");
            }
        };

        self._showNotification = function() {
            var options = {
                title: "Updatefix 1.2.7 active",
                text: "You should now be able to update to OctoPrint 1.2.8 without issues.. For more information on what to expect, see the info dialog.",
                hide: false,
                auto_display: false,
                confirm: {
                    confirm: true,
                    buttons: [{
                        text: "Show info dialog",
                        click: function(notice) {
                            notice.remove();
                            self._showDialog();
                        }
                    }]
                },
                buttons: {
                    show_on_nonblock: true,
                    closer: false,
                    sticker: false
                }
            };

            var notify = new PNotify(options);
            notify.options.confirm.buttons = [notify.options.confirm.buttons[0]];
            notify.modules.confirm.makeDialog(notify, notify.options.confirm);
            notify.open();
        };
    }

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([
        Updatefix127ViewModel,
        [],
        []
    ]);
});
