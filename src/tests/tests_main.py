import device_side

from device_side import config

# Should run without exceptions
try:
	CONFIG = config.Config("./device_side/configuration/.env.example")
except FileNotFoundError:
	assert False
except KeyError:
	assert False
