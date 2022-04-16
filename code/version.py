import logging
import re

from misc import null_logger


def get_version(logger: logging.Logger = null_logger) -> str:
	version_file_name = "../VERSION"
	version_file = open(version_file_name, "r")

	loaded_version_string = version_file.readline()
	version_string_pattern1 = r"[0-9]+\.[0-9]+\.[0-9]+"  # eg. 1.10.0
	version_string_pattern2 = r"^\d{4}/(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])$"  # eg. 2022/04/16

	does_version_string_match_pattern1 = re.match(version_string_pattern1, loaded_version_string)
	does_version_string_match_pattern2 = re.match(version_string_pattern2, loaded_version_string)
	does_version_string_match_pattern = does_version_string_match_pattern1 or does_version_string_match_pattern2

	if does_version_string_match_pattern:
		if does_version_string_match_pattern1:
			logger.debug(f"Obtained version string matching the classic pattern. Version: `{loaded_version_string}`")
		if does_version_string_match_pattern2:
			logger.debug(f"Obtained version string matching the YYYY/MM/DD pattern. Version: `{loaded_version_string}`")
	else:
		logger.warning(f"Obtained version string, but it does not match any expected pattern. "
		               f"Version: `{loaded_version_string}`")

	return loaded_version_string
