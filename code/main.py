import logging.config
import tkinter as tk

from dir_selection import TargetDirSelection
from file_selection import TargetFileSelection
from logging_module import logging_config
from version import get_version

logging.config.dictConfig(logging_config)
main_logger = logging.getLogger("MainLogger")


class SelectedDirectory(tk.StringVar):
	"""
	Extension of `tk.StringVar` which is able to call `toggle_directory_set` hook from master on `set`.

	Calls `self.master.toggle_directory_set(True)` when set value is not "none" in which case calls
	`self.master.toggle_directory_set(False)`.
	"""
	def __init__(self, master, enable_hook: bool = True, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self._enable_hook = enable_hook

	def set(self, value: str, *args, **kwargs) -> None:
		super().set(value=value, *args, **kwargs)
		if self._enable_hook:
			if value == "none":
				self.master.toggle_directory_set(False)
			else:
				self.master.toggle_directory_set(True)


class MainFrame(tk.Frame):
	"""
	The File Namer main application Frame.
	"""
	def __init__(self, master, logger=main_logger, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.logger: logging.Logger = logger

		self.selected_directory = SelectedDirectory(master=self, value="none")

		# Creating Directory Selection Frame
		self.dir_select_frame = TargetDirSelection(master=self)
		self.dir_select_frame.grid(column=0, row=0)

	def select_target_dir(self, target_var: str) -> None:
		"""
		Update handler called when target directory has been selected.

		:param dir_selected: has a valid directory been selected or is "none"
		"""
		def when_selected():
			self.file_select_frame.grid(column=0, row=1, pady="0.5cm")

		def when_not_selected():
			self.file_select_frame.grid_remove()

		if dir_selected:
			self.logger.debug("Directory has been selected - showing relevant Frames.")
			when_selected()
		else:
			self.logger.debug("Directory has not been selected - hiding relevant Frames.")
			when_not_selected()


if __name__ == "__main__":
	main_logger.info("Starting File Namer.")

	# Initialise a window
	window = tk.Tk()

	# Set window size
	window.geometry("600x500")
	window.resizable(height=False, width=False)

	# Set the window title and icon
	window.title("File Namer")
	icon = tk.PhotoImage(file="../graphics/potat.png")
	window.iconphoto(True, icon)

	main_frame = MainFrame(window)
	main_frame.pack(padx="1cm", pady="0.5cm")

	main_logger.info(f"Version: `{get_version(main_logger)}`")
	window.mainloop()
