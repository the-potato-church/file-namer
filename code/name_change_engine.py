import ast
import os.path


class NameChangeEngine:
	def __init__(self, master, logger=None):
		self.master = master
		if logger:
			self.logger = logger
		else:
			self.logger = self.master.logger

		self.target_dir = None
		self.target_files = None
		self.name_modifications = None

		self._preprocessed_modifications = None
		self.modified_names = None

	def load_preview(self):
		self.logger.debug("Loading name change preview from NameChangeEngine into NameChangePreview.")
		self.master.first_preview.set(self.modified_names[0])
		self.master.whole_preview.set(self.modified_names)

	def execute(self) -> None:
		"""

		"""
		self.logger.info("Executing name change!")

		if isinstance(self.target_dir, tuple) or isinstance(self.target_dir, list):
			target_dir = self.target_dir[0]
		else:
			target_dir = self.target_dir

		for index, target_file in enumerate(self.target_files):
			full_target_file = os.path.join(target_dir, target_file)
			full_new_name = os.path.join(target_dir, self.modified_names[index])

			self.logger.info(f"Turning `{full_target_file}` into `{full_new_name}`.")
			os.rename(full_target_file, full_new_name)
			self.logger.debug("Rename done and successful.")

		self.master.execute_button["state"] = "disabled"
		self.logger.info("Finished name change!")

	def load_targets_and_modifications(self):
		self.logger.debug("Loading targets and modifications into the NameChangeEngine.")

		self.target_dir = self.master.master.selected_directory.get()
		self.target_files = list(self.master.master.selected_files.get())
		self.name_modifications = list(self.master.master.name_pattern_modifications.get())

		self._preprocessed_modifications = self._preprocess_modifications()
		self.modified_names = [self._process_name_change(name) for name in self.target_files]

	def _preprocess_modifications(self):
		"""
		As the list of modifications from `NamePatternSelection` does not take into account how indeces will change
		as a result of deletions, the list of modifications needs to be modified
		and "processed" for the `NameChangeEngine`.

		:return: list of preprocessed modifications
		"""
		_preprocessed_modifications = self.name_modifications

		for index, modification in enumerate(_preprocessed_modifications):
			# annoyingly, the tk.Variable and it's derivatives insist on giving tuple of strings even if a
			# list of dictionaries has been passed to it... (maybe I am doing something wrong - who knows)

			# if the modifications is still a string - convert it into a dict
			if isinstance(modification, str):
				modification = ast.literal_eval(modification)
			_preprocessed_modifications[index] = modification

			# if the modification is a deletion, it will shift indeces all following modifications
			# thus the need to adjust for it
			if modification["modification"] == "deletion":
				deletion_len = int(modification["end"]) - int(modification["start"])

				# if this modification is last in the chain - there is nothing else following to modify
				if len(_preprocessed_modifications)-1 > index:
					# select all following modifications
					following_modifications = _preprocessed_modifications[index+1:]

					for following_index, following_modification in enumerate(following_modifications, start=index+1):
						# ensure they are all dicts again
						if isinstance(following_modification, str):
							following_modification = ast.literal_eval(following_modification)
						preprocessed_modification = following_modification

						# adjust the modification positions
						preprocessed_start = str(int(following_modification["start"]) - deletion_len)
						preprocessed_end = str(int(following_modification["end"]) - deletion_len)

						preprocessed_modification["start"] = preprocessed_start
						preprocessed_modification["end"] = preprocessed_end

						# save
						_preprocessed_modifications[following_index] = preprocessed_modification

		self.logger.debug(f"Preprocessed name modifications: {_preprocessed_modifications}.")
		return _preprocessed_modifications

	def _process_name_change(self, name_to_change: str) -> str:
		"""
		Processes given name using the NameChangeEngine's list of preprocessed
		(see `self._preprocess_modifications`) modifications.

		:param name_to_change: name to process
		:return: processed name
		"""
		self.logger.debug(f"Processing name change for `{name_to_change}`.")

		for modification in self._preprocessed_modifications:
			if modification["modification"] == "addition":
				start = int(modification["start"])
				text_to_add = modification["inserted_text"]

				name_to_change = name_to_change[:start] + text_to_add + name_to_change[start:]

			elif modification["modification"] == "deletion":
				start = int(modification["start"])
				end = int(modification["end"])

				name_to_change = name_to_change[:start] + name_to_change[end:]

		self.logger.debug(f"Processed name modifications. Result: `{name_to_change}`.")
		return name_to_change
