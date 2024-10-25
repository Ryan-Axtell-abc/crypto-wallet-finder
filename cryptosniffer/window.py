from gi.repository import Gtk, Gio, Adw, GLib

from cryptosniffer.const import Constants
from cryptosniffer.functions import update_drive_objects
from cryptosniffer.functions import make_drive
from cryptosniffer.functions import add_custom_styling
from cryptosniffer.functions import load_css
from cryptosniffer.functions import drive_name_to_letter_windows
from cryptosniffer.functions import drive_name_to_letter_linux
from cryptosniffer.functions import if_valid_linux
from cryptosniffer.functions import if_valid_windows

from cryptosniffer.ui_setting_functions import update_drive_cards

import subprocess
import threading
import time
import os
import psutil
#import platform
#from pathlib import Path

class drive_class:
	def __init__(self):
		self.name = None
		self.mount_point = None
		self.is_visible = False
		self.has_windows = False
		self.has_linux = False
		self.size = 0
		self.state = None
		self.start_time = 0
		self.last_finished_time = 0
		self.status = "READY"
		self.results_label = "Search Status: Not ran yet"
		self.ui_card = None
	
	def clear(self):
		self.name = None
		self.mount_point = None
		self.is_visible = False
		self.has_windows = False
		self.has_linux = False
		self.size = 0
		self.state = None
		self.start_time = 0
		self.last_finished_time = 0
		self.status = "READY"
		self.results_label = "Search Status: Not ran yet"
		self.ui_card = None

GLOBALS = {
    "drive_object_map": {},
    "drive_card_map": {},
    "valid_partitions": set(),
	"platform" : "linux",
}

if os.name == "nt":
	GLOBALS["platform"] = "windows"


@Gtk.Template(resource_path=f'{Constants.PATHID}/ui/main.ui')
class MainWindow(Adw.ApplicationWindow):
	__gtype_name__ = "MainWindow"

	main_content = Gtk.Template.Child()
	flap = Gtk.Template.Child()
	stack = Gtk.Template.Child()
	stack_switch = Gtk.Template.Child()
	# Page1 widgets
	page1_box = Gtk.Template.Child()
	#page1_switch = Gtk.Template.Child()
	page1_content = Gtk.Template.Child()
	content_box = Gtk.Template.Child()
	usb_holder = Gtk.Template.Child()
	warning_box = Gtk.Template.Child()
	warning_label = Gtk.Template.Child()
	unmount_button = Gtk.Template.Child()
	secondary_button_toggle_switch = Gtk.Template.Child()
	audio_toggle_switch = Gtk.Template.Child()
	default_search_depth_picker = Gtk.Template.Child()
	default_theme_picker = Gtk.Template.Child()


	def __init__(self, **kwargs):
		Adw.ApplicationWindow.__init__(self, **kwargs)

		# # setup menu actions
		self.create_action('about', self.menu_handler)
		self.create_action('quit', self.menu_handler)

		GLOBALS['css_provider'] = load_css()
		add_custom_styling(GLOBALS, self.main_content)

		#My stuff start

		self.style_manager = Adw.StyleManager().get_default()

		#Make a series of drives inside the USB horizontal box
		self.usb_holder.set_spacing(20)
		self.usb_holder.set_margin_start(10)
		self.usb_holder.set_margin_end(10)

		GLOBALS['ui_card_holder'] = self.usb_holder
		
		for i in range(ord('a'), ord('z')+1):
			letter = chr(i).upper()
			#print("letter:", letter)
			drive_object = drive_class()
			GLOBALS['drive_object_map'][letter] = drive_object
			make_drive(self.usb_holder, letter, GLOBALS)

		time_manager_thread = threading.Thread(target=self.time_manager_thread_loop, name='time_manager_thread_loop')
		plugged_in_drives_checker_thread = threading.Thread(target=self.plugged_in_drives_checker_thread_loop, name='plugged_in_drives_checker_thread_loop')
		
		time_manager_thread.setDaemon(True)
		plugged_in_drives_checker_thread.setDaemon(True)

		time_manager_thread.start()
		plugged_in_drives_checker_thread.start()


	def time_manager_thread_loop(self):
		while True:
			GLib.idle_add(update_drive_cards, GLOBALS)
			time.sleep(.1)
	
	def plugged_in_drives_checker_thread_loop(self):
		known_devices = set()
		while True:
			current_devices = set(part.device for part in psutil.disk_partitions())
			if known_devices !=  current_devices:
				new_drives = current_devices - known_devices
				valid_new_drives = set()
				new_drive_letters = set()
				for drive in new_drives:
					if if_valid_windows(drive):
						letter = drive_name_to_letter_windows(drive)
						new_drive_letters.add(letter)
						valid_new_drives.add(drive)
					elif if_valid_linux(drive):
						letter = drive_name_to_letter_linux(drive)
						new_drive_letters.add(letter)
						valid_new_drives.add(drive)
				
				old_drives = known_devices - current_devices
				valid_old_drives = set()
				old_drive_letters = set()
				for drive in old_drives:
					if if_valid_windows(drive):
						letter = drive_name_to_letter_windows(drive)
						old_drive_letters.add(letter)
						valid_old_drives.add(drive)
					elif if_valid_linux(drive):
						letter = drive_name_to_letter_linux(drive)
						old_drive_letters.add(letter)
						valid_old_drives.add(drive)

				GLOBALS['valid_partitions'].update(valid_new_drives)
				GLOBALS['valid_partitions'].difference_update(valid_old_drives)

				GLOBALS["new_drive_letters"] = new_drive_letters
				GLOBALS["old_drive_letters"] = old_drive_letters
				
				update_drive_objects(GLOBALS)
				GLib.idle_add(update_drive_cards, GLOBALS)
			
			known_devices = current_devices
			time.sleep(.05)
	

	@Gtk.Template.Callback()
	def on_color_switch(self, *args):
		if self.style_manager.get_dark():
			self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
		else:
			self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

	@Gtk.Template.Callback()
	def on_flap_toggled(self, widget):
		self.flap.set_reveal_flap(not self.flap.get_reveal_flap())


	def menu_handler(self, action, state):
		""" Callback for  menu actions"""
		name = action.get_name()
		print(f'active : {name}')
		if name == 'quit':
			self.close()
		elif name == 'about':
			self.show_about_window()
	
	def show_about_window(self, *_args):
		#windows = list_toplevels()
		main_window = None
		toplevels = Gtk.Window.list_toplevels()
		for window in toplevels:
			print(window)
			if window.is_active():
				main_window = window
		about = Adw.AboutWindow(
			transient_for=main_window,
			application_name=_("CryptoSniffer"),
			application_icon="bitcoin",
			developer_name=_("PCI Computers, made for Glen Sebring"),
			website="https://www.pcichico.com/",
			#support_url="help_url",
			#issue_url="bugtracker_url",
			developers=[
				"Ryan https://www.pcichico.com/",
			],
			designers=["Ryan https://www.pcichico.com/"],
			copyright="© 2024 PCI Computers",
			license_type=Gtk.License.GPL_3_0,
			version=1.0,
			release_notes_version=1.0,
			comments=_("This software searches windows hard drives and searches for crypto currency wallets on them.\nSo far it will only tell you if the drive contains a wallet, it won't retrieve it for you.\nSupported wallets:"
			),
		)
		about.add_credit_section(
			_("Sound effects obtained from"),
			[
				"ZAPSPLAT https://www.zapsplat.com",
			],
		)
		about.add_credit_section(
			_("Commisioned by"),
			[
				"Glen Sebring",
			],
		)
		about.add_acknowledgement_section(
			_("Special thanks to"),
			[
				"Glen Sebring",
			],
		)

		about.present()

	def create_action(self, name, callback):
		""" Add an Action and connect to a callback """
		action = Gio.SimpleAction.new(name, None)
		action.connect("activate", callback)
		self.add_action(action)