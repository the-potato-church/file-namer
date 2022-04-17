import logging.config
import tkinter as tk

from dir_selection import TargetDirSelection
from file_selection import TargetFileSelection
from logging_module import logging_config
from version import get_version

logging.config.dictConfig(logging_config)
main_logger = logging.getLogger("MainLogger")


class VarWithHook(tk.Variable):
	"""
	Extension of `tk.Variable` which is able to call supplied hook on `set`.

	If hook is supplied, on `set` it passes the currently set variable to it.
	"""

	def __init__(self, hook=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._file_namer_hook = hook

	def set(self, value) -> None:
		super().set(value=value)
		if self._file_namer_hook:
			self._file_namer_hook(value)


class StringVarWithHook(tk.StringVar):
	"""
	Extension of `tk.StringVar` which is able to call supplied hook on `set`.

	If hook is supplied, on `set` it passes it the currently set variable.
	"""
	def __init__(self, hook=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._file_namer_hook = hook

	def set(self, value: str) -> None:
		super().set(value=value)
		if self._file_namer_hook:
			self._file_namer_hook(value)


class MainFrame(tk.Frame):
	"""
	The File Namer main application `tk.Frame`.
	"""
	def __init__(self, master, logger=main_logger, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.logger: logging.Logger = logger

		self.selected_directory = StringVarWithHook(
			hook=self.after_target_directory_select,
			value="none",
		)
		self.selected_files = VarWithHook(
			hook=self.after_target_file_select,
			value=[],
		)

		# Creating Directory Selection Frame
		self.dir_select_frame = TargetDirSelection(master=self)
		self.dir_select_frame.grid(column=0, row=0)

		# Creating File Selection Frame; shown when target directory is selected (see `self.toggle_directory_set`)
		self.file_select_frame = TargetFileSelection(master=self)

	def after_target_directory_select(self, selected_dir: str) -> None:
		"""
		Update handler called when target directory has been selected.

		:param selected_dir: has a valid directory been selected or is "none"
		"""
		def when_selected():
			self.file_select_frame.grid(column=0, row=1, pady="0.5cm")
			self.file_select_frame.load_files_in_directory()

		def when_not_selected():
			self.file_select_frame.grid_remove()
			self.file_select_frame.load_files_in_directory()

		if selected_dir != "none":
			self.logger.debug("Directory has been selected - showing relevant Frames.")
			when_selected()
		else:
			self.logger.debug("Directory has not been selected - hiding relevant Frames.")
			when_not_selected()

	def after_target_file_select(self, selected_files: list[str]):
		pass


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
