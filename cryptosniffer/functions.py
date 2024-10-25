import os
from gi.repository import Gtk, Gio, Adw, Pango, GLib
from cryptosniffer.const import Constants
import psutil
import subprocess
import threading

import time

def grep(text_list,substring,inverse):
	output_list = []
	if inverse:
		for line in text_list:
			if not substring in line:
				output_list.append(line)
	else:
		for line in text_list:
			if substring in line:
				output_list.append(line)
	return output_list

def seconds_to_minutes(input_seconds):
	input_seconds = int(input_seconds)
	minutes = int(input_seconds/60)
	seconds = int(input_seconds%60)
	if (minutes / 10) < 1:
		minutes = '0'+str(minutes)
	minutes = str(minutes)
	if (seconds / 10) < 1:
		seconds = '0'+str(seconds)
	seconds = str(seconds)
	output = minutes+":"+seconds
	return output

def check_os_install(mountpoint):
	is_windows = os.path.exists(os.path.join(mountpoint, "Windows"))
	is_linux = os.path.exists(os.path.join(mountpoint, "boot")) and os.path.exists(os.path.join(mountpoint, "etc"))
	return is_windows, is_linux

def if_valid_windows(name):
	if ':' in name:
		return True


def drive_name_to_letter_windows(name):
	letter = name
	if ':' in name:
		letter = name.split(':')[0]
		
	return letter

def if_valid_linux(name):
	if '/dev/' in name:
		if '/dev/sd' in name:
			return True

def drive_name_to_letter_linux(name):
	letter = name
	if '/dev/sd' in name:
		letter = name.split('/dev/sd')[1][0]
		letter = letter.upper()
		
	return letter

def get_drive_ui_element(drive, desired_object):

	title_bar_box = drive.get_first_child()
	drive_title = title_bar_box.get_first_child().get_first_child().get_first_child().get_next_sibling()

	status_box = title_bar_box.get_next_sibling()
	status_label_box = status_box.get_first_child()
	status_label = status_label_box.get_first_child()
	
	status_colorful_outer = status_label_box.get_last_child()
	status_colorful_inner = status_colorful_outer.get_first_child()
	status_result_text = status_colorful_inner.get_first_child()

	output_scrolled_window = status_label_box.get_next_sibling()
	info_box = output_scrolled_window.get_first_child().get_first_child()
	centered_info_box = info_box.get_first_child()
	
	drive_general_path_box = centered_info_box.get_first_child()

	mounted_box = drive_general_path_box.get_first_child()
	mounted_image = mounted_box.get_first_child()
	mounted_link = mounted_box.get_last_child()


	unmounted_box = mounted_box.get_next_sibling()
	unmounted_image = unmounted_box.get_first_child()
	unmounted_text = unmounted_box.get_last_child()

	path_box = unmounted_box.get_next_sibling()
	path_image = path_box.get_first_child()
	path_text = path_box.get_last_child()

	search_status_box = drive_general_path_box.get_next_sibling()
	search_status = search_status_box.get_first_child()

	button_v_box = status_box.get_next_sibling()
	button_v_filler_box = button_v_box.get_first_child()
	button_h_box = button_v_filler_box.get_next_sibling()
	button = button_h_box.get_first_child()

	if desired_object == "drive_title":
		return drive_title
	elif desired_object == "status_box":
		return status_box
	elif desired_object == "status_label_box":
		return status_label_box
	elif desired_object == "status_label":
		return status_label
	elif desired_object == "status_colorful_outer":
		return status_colorful_outer
	elif desired_object == "status_colorful_inner":
		return status_colorful_inner
	elif desired_object == "status_result_text":
		return status_result_text
	elif desired_object == "info_box":
		return info_box
	elif desired_object == "mounted_box":
		return mounted_box
	elif desired_object == "mounted_image":
		return mounted_image
	elif desired_object == "mounted_link":
		return mounted_link
	elif desired_object == "unmounted_box":
		return unmounted_box
	elif desired_object == "unmounted_image":
		return unmounted_image
	elif desired_object == "unmounted_text":
		return unmounted_text
	elif desired_object == "path_box":
		return path_box
	elif desired_object == "path_image":
		return path_image
	elif desired_object == "path_text":
		return path_text
	elif desired_object == "search_status_box":
		return search_status_box
	elif desired_object == "search_status":
		return search_status
	elif desired_object == "button":
		return button


def make_drive(parent, letter, GLOBALS):
	#letter = chr(ord('A') + number - 1)
	#print("number:", number, "letter:", letter)
	drive = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	parent.append(drive)

	drive.add_css_class("box_shadow")
	drive.add_css_class("drive")

	#make title bar box
	title_bar_box = Gtk.ActionBar()
	drive.append(title_bar_box)
	
	#make drive label
	drive_title = Gtk.Label()
	drive_title.set_text("Disk "+str(letter))
	drive_title.add_css_class("heading")
	title_bar_box.set_center_widget(drive_title)

	#make eject button
	eject_button = Gtk.Button()
	test_text = Gtk.Image()
	test_text.set_from_icon_name("media-eject-symbolic")
	eject_button.set_child(test_text)
	#eject_button.set_icon_name("media-eject-symbolic")
	title_bar_box.pack_end(eject_button)
	eject_button.connect('clicked', lambda widget: click_eject_button(eject_button, GLOBALS))

	actionbar = title_bar_box
	revealer = actionbar.get_first_child()
	box = revealer.get_first_child()
	box_first_child = box.get_first_child()
	box_middle_child = box_first_child.get_next_sibling()
	box_last_child = box.get_last_child()

	#actionbar.add_css_class("blank")
	#revealer.add_css_class("blank")
	box.add_css_class("blank")
	box_last_child.get_first_child().add_css_class("zero-margin")

	#make status box
	status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	drive.append(status_box)
	#status_box.add_css_class("green")
	##make status label section
	#make status label box
	status_label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	status_box.append(status_label_box)
	#make status label ("status: " text), child of status label box
	status_label = Gtk.Label()
	status_label.set_text("Status: ")
	status_label_box.append(status_label)

	#make status label box border (border for bitcoin effect), next child of status label box
	status_colorful_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	status_label_box.append(status_colorful_outer)
	status_colorful_outer.add_css_class("holder_border_theme_base")
	
	#make status label box (gradient bitcoin effect)
	status_colorful_inner = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	status_colorful_outer.append(status_colorful_inner)
	status_colorful_inner.add_css_class("holder_theme_base")
	
	status_colorful_inner.set_hexpand(True)
	#make status result label (bitcoin text)
	status_result_text = Gtk.Label()

	status_colorful_inner.append(status_result_text)
	

	#Make output scrolled window
	output_scrolled_window = Gtk.ScrolledWindow()
	output_scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

	output_scrolled_window.set_min_content_height(192)
	output_scrolled_window.set_max_content_width(80)
	#output_scrolled_window.add_css_class("gold")
	#output_scrolled_window.add_css_class("scrolled_window")
	output_scrolled_window.add_css_class("rounded")
	output_scrolled_window.set_margin_top(10)
	
	status_box.append(output_scrolled_window)

	#make info box
	info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	info_box.set_valign(Gtk.Align.CENTER)
	info_box.set_vexpand(False)
	info_box.add_css_class("info_box")
	output_scrolled_window.set_child(info_box)
	

	#make info box
	centered_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	centered_info_box.set_valign(Gtk.Align.CENTER)
	centered_info_box.set_vexpand(True)
	centered_info_box.add_css_class("centered_info_box")
	
	info_box.append(centered_info_box)

	drive_general_path_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	drive_general_path_box.add_css_class("rounded")
	drive_general_path_box.set_margin_bottom(10)
	
	centered_info_box.append(drive_general_path_box)

	mounted_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	mounted_box.set_halign(Gtk.Align.CENTER)
	drive_general_path_box.append(mounted_box)

	mounted_image = Gtk.Image()


	#mounted_image.add_css_class("sub_text")
	
	mounted_box.append(mounted_image)

	mounted_link = Gtk.LinkButton()
	mounted_link.add_css_class("sub_text")
	mounted_link.add_css_class("neutralize_link_spacing")
	mounted_link.set_margin_start(3)
	
	mounted_box.append(mounted_link)

	unmounted_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	unmounted_box.set_halign(Gtk.Align.CENTER)
	drive_general_path_box.append(unmounted_box)

	
	unmounted_image = Gtk.Image()
	unmounted_image.set_from_icon_name("drive-harddisk-symbolic")
	unmounted_image.add_css_class("sub_text")
	
	unmounted_box.append(unmounted_image)

	unmounted_text = Gtk.Label()
	unmounted_text.set_text("200GB")
	unmounted_text.set_margin_start(3)
	unmounted_text.add_css_class("sub_text")
	
	unmounted_box.append(unmounted_text)

	path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	path_box.set_halign(Gtk.Align.CENTER)
	drive_general_path_box.append(path_box)

	path_image = Gtk.Image()
	path_image.set_from_icon_name("drive-harddisk-symbolic")
	path_image.add_css_class("sub_text")
	
	path_box.append(path_image)

	path_text = Gtk.Label()
	path_text.set_text("test")
	path_text.set_margin_start(3)
	path_text.add_css_class("sub_text")
	
	path_box.append(path_text)
	path_box.set_visible(False)

	search_status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	search_status_box.add_css_class("foreground_color")
	search_status_box.add_css_class("rounded")
	
	centered_info_box.append(search_status_box)


	#search_status = Gtk.Label()
	#search_status.set_text("Search Status: Not ran yet")
	#search_status.add_css_class("sub_text")

	search_status = Gtk.TextView()
	search_status.set_editable(False)
	search_status.set_cursor_visible(False)
	search_status.add_css_class("sub_text")
	
	#search_status.set_max_width_chars(10)
	#search_status.set_wrap(True)

	search_status_gesture = Gtk.GestureClick.new()
	search_status_gesture.connect("released", lambda gesture, n_press, x, y: on_search_status_click(gesture, n_press, x, y, GLOBALS, drive))
	search_status.add_controller(search_status_gesture)
	
	search_status_box.append(search_status)
	#search_status_box.append(textview)


	textview_buffer = search_status.get_buffer()
	link_tag = textview_buffer.create_tag("link_tag", foreground="blue", underline=Pango.Underline.SINGLE)

	#make button box
	button_v_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	drive.append(button_v_box)


	#make button filler box
	button_v_filler_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	button_v_box.append(button_v_filler_box)
	button_v_filler_box.set_vexpand(True)

	button_h_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	button_v_box.append(button_h_box)

	#make GtkSizeGroup for buttons
	button_size_group = Gtk.SizeGroup()


	#make control button
	button = Gtk.Button(label="Start")
	button.set_hexpand(True)
	button_h_box.append(button)
	button.connect('clicked', lambda widget: click_search_button(button, GLOBALS))

	button_size_group.add_widget(button)

	
	add_custom_styling(GLOBALS, drive)

	drive_object = GLOBALS['drive_object_map'][letter]
	#print("drive_object:", drive_object)
	drive_object.ui_card = drive
	#print("drive_object.ui_card:", drive_object.ui_card)
	GLOBALS['drive_card_map'][letter] = drive

def update_drive_objects(GLOBALS):
	valid_partitions = GLOBALS['valid_partitions']
	drive_object_map = GLOBALS['drive_object_map']
	new_drive_letters = GLOBALS['new_drive_letters']
	old_drive_letters = GLOBALS['old_drive_letters']


	partition_objects = []
	for partition in psutil.disk_partitions():
		if partition.device in valid_partitions:
			partition_objects.append(partition)

	print("partition_objects:",partition_objects)

	for key in new_drive_letters:
		drive_object = drive_object_map[key]
		drive_object.clear()
		
	for key in old_drive_letters:
		drive_object = drive_object_map[key]
		drive_object.clear()
		ui_card = GLOBALS['drive_card_map'][key]
		textview = get_drive_ui_element(ui_card, "search_status")
		textview_buffer = textview.get_buffer()
		# Start the ping process
		textview_buffer.set_text("")
	
	for partition in partition_objects:

		total_size = 0

		try:
			usage = psutil.disk_usage(partition.mountpoint)
			total_size = usage.total
		except:
			continue
		
		name = partition.device
		print("name:",name)
		print("total_size:",total_size)


		if if_valid_windows(name):
			letter = drive_name_to_letter_windows(name)
		elif if_valid_linux(name):
			letter = drive_name_to_letter_linux(name)
		else:
			print("PROBLEM: BAD DRIVE SNUCK THROUGH")
			
		print("letter:",letter)
		
		drive_object = drive_object_map[letter]
		
		has_windows, has_linux = check_os_install(partition.mountpoint)
		print("letter:", letter)
		print("has_windows:", has_windows)
		#print("has_linux:", has_linux)

		drive_object.name = name
		drive_object.mount_point = partition.mountpoint
		#print("new_drive_letters:", new_drive_letters)
		if letter in new_drive_letters:
			drive_object.is_visible = True
		drive_object.has_windows = has_windows
		drive_object.has_linux = has_linux
		drive_object.size = total_size

		if GLOBALS["platform"] == "windows" and letter == 'C':
			print("I am here")
			drive_object.is_visible = False


def add_custom_styling(GLOBALS, widget):
	add_widget_styling(GLOBALS, widget)
	# iterate children recursive
	for child in widget:
		add_custom_styling(GLOBALS, child)

def add_widget_styling(GLOBALS, widget):
	if GLOBALS['css_provider']:
		# print(f'Adding style to : {widget.props.css_name}')
		context = widget.get_style_context()
		context.add_provider(
			GLOBALS['css_provider'], Gtk.STYLE_PROVIDER_PRIORITY_USER)

def load_css():
	"""create a provider for custom styling"""
	css_provider = Gtk.CssProvider()
	css_path = f'{Constants.PATHID}/css/main.css'
	try:
		css_provider.load_from_resource(resource_path=css_path)
	except GLib.Error as e:
		print(f"Error loading CSS : {e} ")
		return None
	print(f'loading custom styling from resource: {css_path}')
	# print(css_provider.to_string())
	return css_provider

def convert_size(size_bytes):
	# Conversion to human-readable units
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB")
	i = int(min(len(size_name) - 1, (size_bytes.bit_length() - 1) // 10))
	p = 1 << (i * 10)
	return f"{size_bytes / p:.2f} {size_name[i]}"

def click_eject_button(button, GLOBALS):
	from cryptosniffer.ui_setting_functions import update_drive_cards

	drive = button.get_parent().get_parent().get_parent().get_parent().get_parent()
	name = get_drive_ui_element(drive, "drive_title").get_text()
	letter = name.replace("Disk ", '')

	drive_object_map = GLOBALS['drive_object_map']
	drive_object = drive_object_map[letter]
	drive_object.is_visible = False
	GLib.idle_add(update_drive_cards, GLOBALS)


def click_search_button(button, GLOBALS):
	drive_object_map = GLOBALS['drive_object_map']

	drive = button.get_parent().get_parent().get_parent()
	name = get_drive_ui_element(drive, "drive_title").get_text()
	letter = name.replace("Disk ", '')
	drive_object = drive_object_map[letter]
	current_state = drive_object.state

	if current_state == "searching":
		drive_object.state = "done"
		drive_object.status = "CANCELED"
		button.set_label("Start")
		print("Canceled early")
	else:
		#start search
		drive_object.state = "searching"
		drive_object.status = "RUNNING"
		button.set_label("Cancel")
		drive_object.start_time = time.time()
		thread = threading.Thread(target=run_search,  args=(GLOBALS, letter), daemon=True)
		thread.start()

def on_search_status_click(gesture, n_press, x, y, GLOBALS, ui_card):
	search_status = get_drive_ui_element(ui_card, "search_status")
	textview_buffer = search_status.get_buffer()
	tag_table = textview_buffer.get_tag_table()
	link_tag = tag_table.lookup("link_tag")

	text_iter = search_status.get_iter_at_location(int(x), int(y))[1]

	tags = text_iter.get_tags()
	print("##############")
	for tag in tags:
		print("tag:", tag)
	print("##############")

	# Check if the text at the clicked position has the tag
	if link_tag in tags:

		# Get the clicked text (directory)
		start_iter = text_iter.copy()
		end_iter = text_iter.copy()

		# Move the iterators to the start and end of the line (instead of word)
		start_iter.set_line_offset(0)  # Move to the start of the current line
		end_iter.forward_to_line_end()  # Move to the end of the current line

		# Retrieve the text between start_iter and end_iter, which should be the full directory
		directory = textview_buffer.get_text(start_iter, end_iter, True).strip()

		# Open the directory
		open_directory(GLOBALS, directory)

def open_directory(GLOBALS, directory):
	abs_directory = os.path.abspath(directory)
	print("abs_directory:", abs_directory)
	if GLOBALS["platform"] == "linux": 
		print("directory:", directory)
		os.system(f'xdg-open "{directory}"')
	elif GLOBALS["platform"] == "windows":
		os.startfile(directory)

def append_output(ui_card, directory):

	#I need textview_buffer and I need link_tag
	search_status = get_drive_ui_element(ui_card, "search_status")
	textview_buffer = search_status.get_buffer()
	tag_table = textview_buffer.get_tag_table()
	link_tag = tag_table.lookup("link_tag")
	#print("link_tag:",link_tag )

	end_iter = textview_buffer.get_end_iter()
	textview_buffer.insert_with_tags(end_iter, f"{directory}\n", link_tag)

	end_iter = textview_buffer.get_end_iter()



def run_search(GLOBALS, letter):
	ui_card = GLOBALS['drive_card_map'][letter]
	drive_object = GLOBALS['drive_object_map'][letter]
	textview = get_drive_ui_element(ui_card, "search_status")
	
	textview_buffer = textview.get_buffer()
	# Start the ping process
	textview_buffer.set_text("")

	if GLOBALS["platform"] == "windows":
		exe_path = r"C:\ES\es.exe"
		exe_args = "-path "+str(letter)+":/ "+"-r "+"'Bitcoin|Bither|MultiBit|Armory|Electrum|Exodus|FeatherWallet|monero|MyCrypto|Sparrow|Specter|WalletWasabi|^wallets$|\.wallet$'"
		powershell_command = f'& "{exe_path}" {exe_args}'
		process = subprocess.Popen(
			["powershell", "-Command", powershell_command],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True
		)
	else:
		exe_path = r"C:\ES\es.exe"
		exe_args = "-path "+str(letter)+":/ "+"-r "+"'Bitcoin|Bither|MultiBit|Armory|Electrum|Exodus|FeatherWallet|monero|MyCrypto|Sparrow|Specter|WalletWasabi|^wallets$|\.wallet$'"
		powershell_command = f'& "{exe_path}" {exe_args}'
		bash_command = 'for i in {1..10}; do echo hi $i; sleep .3; done'
		bash_command = 'ping 4chan.org'
		bash_command = 'for i in {1..10}; do echo /mnt/HDD/; sleep .3; done'
		
		process = subprocess.Popen(
			bash_command,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			executable='/bin/bash',
			shell=True
		)

	# Read the output in real time
	has_output = False
	for line in process.stdout:
		if drive_object.status == "CANCELED":
			process.kill()
			break
		has_output = True
		print("THIS IS A WHOLE LINE")
		print(line)
		print("END")
		GLib.idle_add(append_output, ui_card, line.strip())
	
	# Close process when done
	process.wait()
	if drive_object.status == "CANCELED":
		pass
	else:
		drive_object.status = "FINISHED"
	
	drive_object.state = "done"
	drive_object.last_finished_time = time.time() - drive_object.start_time
	return False 
