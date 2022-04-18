import tkinter as tk
from tkinter import filedialog


class TargetDirSelection(tk.Frame):
	"""
	Frame handling the selection of Target Directory.

	Contains:
		- target directory selection button
		- label showing the currently selected directory

	Requirements from 'master':
		- master.selected_directory: tk.StringVar
		- master.logger: logging.Logger | supply logger on initialisation
	"""
	def __init__(self, master, logger=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		if logger:
			self.logger = logger
		else:
			self.logger = self.master.logger

		# Target Directory selection button
		self.select_button = tk.Button(
			master=self,
			text="Select target directory",
			command=self.select_directory,
		)
		self.select_button.grid(column=0, row=0)

		self.selected_directory = self.master.selected_directory
		self.selected_directory_label = self.SelectedDirectoryLabel(
			master=self,
			padx="3mm",
		)
		self.selected_directory_label.grid(column=1, row=0)

	class SelectedDirectoryLabel(tk.Frame):
		"""
		Shows the currently selected target directory.
		"""
		def __init__(self, master, logger=None, *args, **kwargs):
			super().__init__(master, *args, **kwargs)
			self.master = master
			if logger:
				self.logger = logger
			else:
				self.logger = self.master.logger

			self.selected_directory_label_prefix = tk.Label(
				master=self,
				text="Selected target directory:",
			)
			self.selected_directory_label_prefix.grid(column=0, row=0)

			self.selected_directory_label = tk.Label(
				master=self,
				textvariable=self.master.selected_directory,
			)
			self.selected_directory_label.grid(column=1, row=0)

	def select_directory(self):
		directory = filedialog.askdirectory(initialdir="/", title="Select Target Directory")
		if directory != "":
			self.logger.info(f"Selected target directory: `{directory}`.")
			self.master.selected_directory.set(directory)
		else:
			self.logger.info("No directory selected.")
			self.master.selected_directory.set("none")
