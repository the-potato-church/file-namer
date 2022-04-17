import logging
import os
import tkinter as tk


class TargetFileSelection(tk.Frame):
	"""

	"""
	def __init__(self, master, logger: logging.Logger = None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		if logger:
			self.logger = logger
		else:
			self.logger = self.master.logger

		# Creating Title Frame
		self.title_frame = tk.Frame(master=self)
		self.title_frame.grid(column=0, row=0, sticky="W")

		self.title = tk.Label(
			master=self.title_frame,
			text="Select Target Files.",
		)
		self.title.pack()

		# Creating File Select Frame
		self.file_select_frame = tk.Frame(master=self)
		self.file_select_frame.grid(column=0, row=1, padx="0.5cm", pady="0.2cm")

		self.files_in_directory = tk.Variable(value=self._get_files_in_directory())
		self.file_listbox = tk.Listbox(
			master=self.file_select_frame,
			width=70,
			listvariable=self.files_in_directory,
			selectmode="extended",
		)
		self.file_listbox.pack()

		self.confirm_file_selection = tk.Button(
			master=self.file_select_frame,
			text="Confirm file selection",
			command=self.select_target_files,
		)
		self.confirm_file_selection.pack(side="left", padx="0.2cm", pady="0.2cm")

	def load_files_in_directory(self) -> None:
		self.logger.debug("Loading files in directory into `self.files_in_directory`")
		self.files_in_directory.set(self._get_files_in_directory())

	def _get_files_in_directory(self) -> list[str]:
		"""
		Loads and returns the list of files in the target directory using `os.listdir()`.
		Checks whether items in the directory actually are files with `os.path.isfile()`.

		:return: list of files in target directory
		"""
		self.logger.debug("Loading list of files in target directory.")

		target_directory = self.master.selected_directory.get()
		if target_directory == "none":
			self.logger.debug("Target directory not yet selected - returning empty list.")
			return []
		else:
			list_of_files_in_directory = [
				item for item in os.listdir(target_directory) if os.path.isfile(target_directory+"/"+item)
			]
			self.logger.debug(f"Loaded a list of files: {list_of_files_in_directory}")
			return list_of_files_in_directory

	def select_target_files(self) -> None:
		"""
		Saves the currently selected files in `self.file_listbox` to the Mainframe's variable `selected_files`.
		"""
		self.master.selected_files.set(self._get_selected_items())

	def _get_selected_items(self) -> list[str]:
		"""
		Returns a list of files currently selected in the `self.file_listbox`
		"""
		self.logger.debug("Fetching the list of files currently selected in `self.file_listbox`.")

		selected_files = [self.file_listbox.get(selected_file) for selected_file in self.file_listbox.curselection()]
		self.logger.debug(f"Loaded the list of selected files in `self.file_listbox`: {selected_files}.")

		return selected_files
