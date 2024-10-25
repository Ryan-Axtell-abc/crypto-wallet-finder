from cryptosniffer.functions import seconds_to_minutes
from cryptosniffer.functions import get_drive_ui_element

import time
import os



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

def status_setter(GLOBALS, ui_card, drive_object):
	
	from cryptosniffer.functions import add_custom_styling

	status_colorful_outer = get_drive_ui_element(ui_card, "status_colorful_outer")
	status_colorful_inner = get_drive_ui_element(ui_card, "status_colorful_inner")
	status_result_text = get_drive_ui_element(ui_card, "status_result_text")

	status_colorful_outer.remove_css_class("gold_border")
	status_colorful_inner.remove_css_class("gold")
	status_result_text.remove_css_class("outline_text")
	status_colorful_outer.remove_css_class("green")
	status_colorful_outer.remove_css_class("blue")
	status_colorful_outer.remove_css_class("grey")
	status_colorful_outer.remove_css_class("running")
	status_result_text.set_opacity(1)

	status = drive_object.status

	status_text = status
	if status == "READY":
		status_colorful_outer.add_css_class("green")
	elif status == "RUNNING":
		status_colorful_outer.add_css_class("running")
		running_time = time.time() - drive_object.start_time
		formatted_running_time = seconds_to_minutes(running_time)
		status_text = "RUNNING - "+formatted_running_time
	elif status == "CANCELED":
		status_colorful_outer.add_css_class("grey")
		finished_time = drive_object.last_finished_time
		formatted_finished_time = seconds_to_minutes(finished_time)
		status_text = "CANCELED - "+formatted_finished_time
	elif status == "FINISHED":
		status_colorful_outer.add_css_class("grey")
		finished_time = drive_object.last_finished_time
		formatted_finished_time = seconds_to_minutes(finished_time)
		status_text = "FINISHED - "+formatted_finished_time

	elif status == "Wallet Found":
		status_colorful_outer.add_css_class("gold_border")
		status_colorful_inner.add_css_class("gold")
		status_result_text.add_css_class("outline_text")
		#os.system('notify-send "Wallet Found"')


		finished_time = time.time() - drive_object.start_time
		formatted_finished_time = seconds_to_minutes(finished_time)
		status_text = "Wallet Found - "+formatted_finished_time
	
	status_result_text.set_text(status_text)

	add_custom_styling(GLOBALS, status_colorful_outer)
	add_custom_styling(GLOBALS, status_colorful_inner)
	add_custom_styling(GLOBALS, status_result_text)


def update_drive_cards(GLOBALS):
	from cryptosniffer.functions import convert_size

	drive_object_map = GLOBALS['drive_object_map']
	drive_card_map = GLOBALS['drive_card_map']


	for key in drive_object_map:
		drive_object = drive_object_map[key]
		ui_card = drive_card_map[key]

		if drive_object.is_visible:
			ui_card.set_visible(True)

			results_label = get_drive_ui_element(ui_card, "search_status")
			#results_label.set_text(drive_object.results_label)

			mounted_link = get_drive_ui_element(ui_card, "mounted_link")
			mounted_image = get_drive_ui_element(ui_card, "mounted_image")

			if drive_object.mount_point:
				mount_path = drive_object.mount_point
			else:
				mount_path = "HI :)"
			display_mount_path = mount_path
			if len(display_mount_path) > 30:
				display_mount_path = mount_path[0:27]+"..."				

			mounted_link.set_label(display_mount_path)
			mounted_link.set_uri('file:///'+mount_path.replace('\\', '/' ))
			
			unmounted_text = get_drive_ui_element(ui_card, "unmounted_text")
			unmounted_text.set_text(convert_size(drive_object.size))

			if drive_object.state == 'searching':
				running_time = time.time()-float(drive_object.start_time)
				formatted_time = seconds_to_minutes(int(running_time))
				status_result_text = get_drive_ui_element(ui_card, "status_result_text")
				status_result_text.set_text(drive_object.status+" - "+formatted_time)
			
			status_setter(GLOBALS, ui_card, drive_object)
		else:
			ui_card.set_visible(False)