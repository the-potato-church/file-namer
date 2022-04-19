import tkinter as tk

from name_change_engine import NameChangeEngine


class NameChangePreview(tk.Frame):
	"""

	"""
	def __init__(self, master, logger=None, *args, **kwargs):
		super().__init__(master, *args, **kwargs)
		self.master = master
		if logger:
			self.logger = logger
		else:
			self.logger = self.master.logger

		# Create Title Frame
		self.title_frame = tk.Frame(master=self)
		self.title_frame.grid(column=0, row=0, sticky="W")

		self.title_label = tk.Label(
			master=self.title_frame,
			text="Preview of changes.",
		)
		self.title_label.pack()

		self.name_change_engine = NameChangeEngine(self)
		self.first_preview = tk.StringVar(value="")
		self.whole_preview = tk.Variable(value=[])

		# Create first file preview frame
		self.preview_label_frame = tk.Frame(master=self)
		self.preview_label_frame.grid(column=0, row=1, pady="0.2cm", sticky="W")

		self.preview_label_prefix = tk.Label(
			master=self.preview_label_frame,
			text="Preview of your first file's new name:",
		)
		self.preview_label_prefix.grid(column=0, row=0)

		self.preview_label = tk.Label(
			master=self.preview_label_frame,
			textvariable=self.first_preview,
			background="#E4EBF1",
		)
		self.preview_label.grid(column=1, row=0, padx="0.1cm")

		# Create whole preview frame
		self.whole_preview_frame = tk.Frame(master=self)
		self.whole_preview_frame.grid(column=0, row=2, pady="0.2cm", sticky="W")

		self.whole_preview_label = tk.Label(
			master=self.whole_preview_frame,
			text="See below the whole preview:"
		)
		self.whole_preview_label.grid(column=0, row=0, pady="0.1cm", sticky="W")

		self.whole_preview_text = tk.Text(
			master=self.whole_preview_frame,
			width=55,
			height=6,
			background="#D6E2EA",
		)
		self.whole_preview_text.grid(column=0, row=1, pady="0.1cm")
		self.whole_preview_text["state"] = "disabled"

		self.execute_button = tk.Button(
			master=self,
			text="Execute name change!",
			command=self.name_change_engine.execute,
		)
		self.execute_button.grid(column=0, row=3, pady="0.2cm")

	def grid(self, *args, **kwargs):
		super().grid(*args, **kwargs)

		self.name_change_engine.load_targets_and_modifications()
		self.name_change_engine.load_preview()

		self.whole_preview_text["state"] = "normal"
		for index, target_file in enumerate(self.name_change_engine.target_files):
			self.whole_preview_text.insert("end", target_file)
			self.whole_preview_text.insert("end", "\n->\n")
			self.whole_preview_text.insert("end", self.name_change_engine.modified_names[index])
			if len(self.name_change_engine.target_files)-1 > index:
				self.whole_preview_text.insert("end", "\n\n")
		self.whole_preview_text["state"] = "disabled"
