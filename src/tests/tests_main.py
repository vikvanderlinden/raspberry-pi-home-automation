import device_side

from device_side import config

CONFIG = config.Config("./device_side/configuration/.env")
# CONFIG.set("database.host", "127.0.0.1")
# CONFIG.set("database.host", "localhost")
print(CONFIG.configuration)
print(CONFIG.get("database.host"))
