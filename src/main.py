# main.py
#
# Copyright 2025 sepehr
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import gi
import logging

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gio, Adw
from .window import SudokuWindow
from .help_dialog import HowToPlayDialog

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class SudokuApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="io.github.sepehr_rs.Sudoku",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.create_action("quit", self.quit, ["<primary>q", "<primary>w"])
        self.create_action("about", self.on_about_action)
        self.create_action("how_to_play", self.on_how_to_play, ["F1"])
        # self.create_action('preferences', self.on_preferences_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *args: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action("win.pencil-toggled", ["<Ctrl>p"])
        self.set_accels_for_action("win.back-to-menu", ["<Ctrl>m"])
        self.set_accels_for_action("win.show-primary-menu", ["F10"])
        # self.set_accels_for_action("app.how_to_play", ["F1"])

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = SudokuWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(
            transient_for=self.props.active_window,
            application_name="Sudoku",
            application_icon="io.github.sepehr_rs.Sudoku",
            developer_name="Sepehr",
            version="1.1.0",
            developers=["Sepehr", "Revisto"],
            copyright="© 2025 sepehr",
        )
        about.present()

    # def on_preferences_action(self, widget, _):
    #     """Callback for the app.preferences action."""
    #     print("app.preferences action activated")

    def on_how_to_play(self, action, param):
        """Show how to play dialog."""
        dialog = HowToPlayDialog(self.props.active_window)
        dialog.get_style_context().add_class("sudoku-dialog")
        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = SudokuApplication()
    return app.run(sys.argv)
