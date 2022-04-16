logging_config = {
	"version": 1,
	"disable_existing_loggers": True,

	"formatters": {
		"default_formatter": {
			"format": "%(asctime)s %(levelname)-8s %(module)-15s %(message)s",
			"datefmt": "%Y-%m-%d %H:%M:%S",
		}
	},

	"handlers": {
		"console": {
			"class": "logging.StreamHandler",
			"formatter": "default_formatter",
			"stream": "ext://sys.stdout",
		},
	},

	"root": {
		"level": "DEBUG",
		"handlers": ["console"]
	},
}
