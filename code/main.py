import logging.config
import tkinter as tk

from dir_selection import TargetDirSelection
from file_selection import TargetFileSelection
from logging_module import logging_config
from name_change_preview import NameChangePreview
from name_pattern_selection import NamePatternSelection
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
		self.name_pattern_modifications = VarWithHook(
			hook=self.after_name_pattern_selected,
			value=[]
		)

		# Creating Directory Selection Frame; initial frame - visible on startup
		self.dir_select_frame = TargetDirSelection(master=self)
		self.dir_select_frame.grid(column=0, row=0)

		# Creating File Selection Frame; shown when target directory is selected
		# (see `self.after_target_directory_select`)
		self.file_select_frame = TargetFileSelection(master=self)

		# Creating Name Pattern Selection Frame; shown when target files are selected
		# (see `self.after_target_file_select`)
		self.name_pattern_select_frame = self._create_new_NamePatternSelection()

		# Creating Name Change Preview Frame; shown when name modifications are confirmed
		# (see `self.after_name_pattern_selected`)
		self.name_change_preview = NameChangePreview(master=self)

	def _create_new_NamePatternSelection(self):
		"""
		An instance of `NamePatternSelection` is called in more than one place.
		This function standardises the instance creation parameters.

		:return: new instance of `NamePatternSelection`
		"""
		return NamePatternSelection(master=self)

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

	def _check_if_target_files_same_length(self, selected_files: list[str]) -> None:
		"""
		A simple check to verify that all target files are the same length.

		At present, the File Namer works with indeces and this will break if not all items have the same number
		of characters (and also the general name pattern - i.e. the key parts of the name
		need to be at the same positions).

		This function is to be deprecated when this stops being the case. todo: deprecate when ready
		"""
		first_length = len(selected_files[0])
		are_all_lengths_same = [len(file) == first_length for file in selected_files]

		self.logger.debug(f"Checking target file name lengths: `{are_all_lengths_same}`.")
		if not all(are_all_lengths_same):
			self.logger.warning("Be careful! I am dumb for now and I can handle "
			                    "only files with the same length and general pattern.")

	def after_target_file_select(self, selected_files: list[str]) -> None:
		self.logger.debug("Target files have been selected - proceeding to name pattern selection.")
		self._check_if_target_files_same_length(selected_files)

		self.dir_select_frame.grid_remove()
		self.file_select_frame.grid_remove()

		self.name_pattern_select_frame.grid(column=0, row=0, padx="1cm", pady="0.5cm")

	def return_to_file_select(self):
		self.logger.debug("Returning from Name Pattern Creation to Target File Selection.")

		# Create a new instance of `NamePatternSelection`
		self.name_pattern_select_frame.destroy()
		self.name_pattern_select_frame = self._create_new_NamePatternSelection()

		# Return to the previous view
		self.dir_select_frame.grid(column=0, row=0)
		self.file_select_frame.grid(column=0, row=1, pady="0.5cm")

	def after_name_pattern_selected(self, name_modifications: list[dict]) -> None:
		self.logger.debug("Name pattern modifications have been selected.")
		self.name_change_preview.grid(column=0, row=2, pady="0.3cm")


if __name__ == "__main__":
	main_logger.info("Starting File Namer.")

	# Initialise a window
	window = tk.Tk()

	# Set window size
	window.geometry("600x550")
	window.resizable(height=False, width=False)

	# Set the window title and icon
	window.title("File Namer")
	icon = tk.PhotoImage(file="../graphics/potat.png")
	window.iconphoto(True, icon)

	main_frame = MainFrame(window)
	main_frame.pack(padx="1cm", pady="0.5cm")

	main_logger.info(f"Version: `{get_version(main_logger)}`.")
	window.mainloop()
