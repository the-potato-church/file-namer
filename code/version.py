import logging
import re

from misc import null_logger


def get_version(logger: logging.Logger = null_logger) -> str:
	version_file_name = "../VERSION"
	version_file = open(version_file_name, "r")

	loaded_version_string = version_file.readline()
	version_string_pattern = r"[0-9]+\.[0-9]+\.[0-9]+"

	does_version_string_match_pattern = re.match(version_string_pattern, loaded_version_string)
	if does_version_string_match_pattern:
		print("Obtained version string.")
	else:
		print("Obtained version string, but it does not match the expected pattern.")

	return loaded_version_string
