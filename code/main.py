import logging.config
import tkinter as tk

from dir_selection import TargetDirSelection
from logging_module import logging_config
from version import get_version

logging.config.dictConfig(logging_config)
main_logger = logging.getLogger("MainLogger")


class MainFrame(tk.Frame):
	"""
	The File Namer main application Frame.
	"""
	def __init__(self, master, logger=main_logger, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		self.logger: logging.Logger = logger

		self.selected_directory = tk.StringVar(value="none")
		self._target_dir_selected = False

		# Creating Directory Selection Frame
		self.dir_select_frame = TargetDirSelection(master=self)
		self.dir_select_frame.grid(column=0, row=0)

	def select_target_dir(self, target_var: str) -> None:
		"""
		Method setting the target directory. When a directory is selected, this method also updates the
		`self._target_dir_selected` to True - enables dynamically showing frames only when target directory is selected.

		:param target_var: selected target directory
		"""
		self._target_dir_selected = True
		self.selected_directory.set(target_var)


if __name__ == "__main__":
	main_logger.info("Starting File Namer.")

	# Initialise a window
	window = tk.Tk()
	# Set window size
	window.geometry("600x500")

	# Set the window title and icon
	window.title("File Namer")
	icon = tk.PhotoImage(file="../graphics/potat.png")
	window.iconphoto(True, icon)

	main_frame = MainFrame(window)
	main_frame.pack(padx="1cm", pady="0.5cm")

	main_logger.info(f"Version: `{get_version(main_logger)}`")
	window.mainloop()
