import tkinter as tk


def subtract_indeces(start_idx: str, end_idx: str) -> int:
	start_line, start_char = start_idx.split(".")
	end_line, end_char = end_idx.split(".")

	start_line, start_char = int(start_line), int(start_char)
	end_line, end_char = int(end_line), int(end_char)

	if end_line - start_line != 0:
		raise RuntimeError("Selection is spanning multiple lines. Invalid!")

	return end_char - start_char


def strip_line_num(index: str):
	split = str(index).split(".")
	if split[0] == "1":
		return split[1]
	else:
		raise RuntimeError("Modification has been made to other than the first line. Not allowed!")


class NamePatternSelection(tk.Frame):
	"""

	"""

	# https://coolors.co/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ea4334-9b2226
	# https://coolors.co/ea4334-78a352-5b8e7d-f3a712-d6e2ea
	def __init__(self, master, logger=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		if logger:
			self.logger = logger
		else:
			self.logger = self.master.logger

		# Creating "Back" button Frame
		self.back_button_frame = tk.Frame(master=self)
		self.back_button_frame.grid(column=0, row=0, pady="0.3cm", sticky="W")

		self.back_button = tk.Button(
			master=self.back_button_frame,
			text="Back to file selection",
			command=self.master.return_to_file_select,
		)
		self.back_button.pack(side="left", pady="0.1cm")

		self.warning_label = tk.Label(
			master=self.back_button_frame,
			text="This will delete your progress with the Name Pattern Creation.",
		)
		self.warning_label.pack(side="left", padx="0.1cm")

		# Creating Title Frame
		self.title_frame = tk.Frame(master=self)
		self.title_frame.grid(column=0, row=1, sticky="W")

		self.title = tk.Label(
			master=self.title_frame,
			text="Create the (re)naming pattern.",
		)
		self.title.pack()

		# Creating name pattern text
		self.name_pattern_text = tk.Text(
			master=self,
			width=55,
			height=3,
			background="#D6E2EA",
		)
		self.name_pattern_text.grid(column=0, row=2, pady="0.1cm", padx="0.1cm", sticky="W")

		# Creating text tags
		self.name_pattern_text.tag_configure("deletion", background="#EA4334")
		self.name_pattern_text.tag_configure("addition", background="#78A352")

		# Creating key bindings
		self.name_pattern_text.bind("<BackSpace>", self._handle_deletion)
		self.name_pattern_text.bind("<space>", self._handle_space)
		self.name_pattern_text.bind("<Key>", self._handle_new_character)

		# Creating pattern confirm button frame
		self.pattern_confirm_button_frame = tk.Frame(master=self)
		self.pattern_confirm_button_frame.grid(column=0, row=3, pady="0.1cm", padx="0.1cm", sticky="W")

		self.pattern_confirm_button = tk.Button(
			master=self.pattern_confirm_button_frame,
			text="Confirm pattern and preview",
			command=self._extract_tags,
		)
		self.pattern_confirm_button.pack(side="left")

		self.edit_pattern_button = tk.Button(
			master=self.pattern_confirm_button_frame,
			text="Edit pattern",
			command=self._return_to_pattern_edit,
		)

	def _get_selection_indeces(self) -> tuple[str, str, bool]:
		try:
			self.logger.debug("Reading `name_pattern_text` selection indeces.")
			start = self.name_pattern_text.index("sel.first")
			end = self.name_pattern_text.index("sel.last")
			move_cursor = False

		except tk.TclError:
			self.logger.debug("There is no text highlighted - using the insert cursor position instead.")
			start = self.name_pattern_text.index("insert-1c")
			end = self.name_pattern_text.index("insert")
			move_cursor = True

		self.logger.debug(f"Selection indeces found: {start}; {end}")
		return start, end, move_cursor

	def _handle_deletion(self, event):
		"""

		"""
		# courtesy of https://stackoverflow.com/a/40841959

		if self.name_pattern_text["state"] == "disabled":
			return "break"

		start, end, move_cursor = self._get_selection_indeces()
		tag = list(self.name_pattern_text.tag_names(start))
		if "sel" in tag:
			tag.remove("sel")

		# If the characters being deleted are a part of the original name without any tags - marking for deletion.
		if len(tag) == 0:
			self.logger.debug("Marking selected character(s) for deletion.")
			self.name_pattern_text.tag_add("deletion", start, end)

			if move_cursor:
				self.logger.debug("Moving the insert cursor one character over.")
				self.name_pattern_text.mark_set("insert", start)

		else:
			self.logger.debug(f"There are tags present in selection. Tag: {tag}")

			# Else - if the segments were added, just delete them
			if "addition" in tag:
				self.logger.debug("Already marked as addition.")
				if subtract_indeces(start, end) == 1:
					self.logger.debug("Selected characters are not part of the original name. Deleting.")
					self.name_pattern_text.delete(start, end)

			# Else - if they were marked for deletion previously, remove the tag
			if "deletion" in tag:
				self.logger.debug("Already marked as deletion.")
				if subtract_indeces(start, end) == 1:
					self.logger.debug("Selected characters were already marked for deletion. Removing deletion tag.")
					self.name_pattern_text.tag_remove("deletion", start, end)

		return "break"

	def _handle_space(self, event):
		"""

		"""
		if self.name_pattern_text["state"] == "disabled":
			return "break"

		self.logger.debug("Adding a ' ' (space) to the file name pattern at the position of the insert cursor.")
		self.name_pattern_text.insert("insert", " ")

		self.logger.debug("Marking the added ' ' (space) as added character.")
		self.name_pattern_text.tag_add("addition", "insert-1c", "insert")

		return "break"

	def _handle_new_character(self, event):
		"""

		"""
		if self.name_pattern_text["state"] == "disabled":
			return "break"

		char = getattr(event, "char", "")
		if len(char) > 0:
			self.logger.debug(f"Adding a '{char}' to the file name pattern at the position of the insert cursor.")
			self.name_pattern_text.insert("insert", char)

			self.logger.debug(f"Marking the added '{char}' as added character.")
			self.name_pattern_text.tag_add("addition", "insert-1c", "insert")

			return "break"
		else:
			self.logger.debug("A non-character key has been pressed. Moving on.")

	def _extract_tags(self) -> None:
		"""

		"""
		tags = list(self.name_pattern_text.tag_names())
		if "sel" in tags:
			tags.remove("sel")
		self.logger.debug(f"Tags: {tags}.")

		modifications = []
		for tag in tags:
			indeces = self.name_pattern_text.tag_ranges(tag)
			self.logger.debug(f"Listing indeces for {tag}: {indeces}")

			if len(indeces) % 2 == 0:
				for i in range(0, len(indeces) - 1, 2):
					modification = {
							"modification": tag,
							"start": strip_line_num(indeces[i]),
							"end": strip_line_num(indeces[i+1]),
						}

					if tag == "addition":
						start, end = modification["start"], modification["end"]
						inserted_text = self.name_pattern_text.get("1."+start, "1."+end)
						modification["inserted_text"] = inserted_text

					modifications += [modification]

			else:
				self.logger.error(f"Tag `{tag}` has an odd number of indeces - not sure what to do! Help!")

		def start_index(modification):
			return int(modification["start"])
		modifications.sort(key=start_index)

		# Disabling `self.name_pattern_text`
		self.name_pattern_text["state"] = "disabled"
		self.pattern_confirm_button["state"] = "disabled"
		self.edit_pattern_button.pack(side="left", padx="0.2cm")

		self.logger.info(f"File naming pattern has been created. Modifications: `{modifications}`.")
		self.master.name_pattern_modifications.set(modifications)

	def _return_to_pattern_edit(self):
		self.name_pattern_text["state"] = "normal"
		self.pattern_confirm_button["state"] = "normal"
		self.edit_pattern_button.pack_forget()

	def grid(self, *args, **kwargs) -> None:
		"""
		Extends the native `tk.Frame` grid method to load the first selected file name into the
		`start_name_pattern_text`.
		"""
		super().grid(*args, **kwargs)

		start_pattern = self.master.selected_files.get()[0]
		self.logger.debug(f"Loaded the starting name pattern - first in the list of target files: `{start_pattern}`.")
		self.name_pattern_text.insert("end", start_pattern)
