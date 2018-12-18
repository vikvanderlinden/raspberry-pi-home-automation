"""
    The config module is able to store configuration items
    optionally loading items from a document.
"""

class Config:
    """
        This class handles the configuration of the application
        A path can be supplied upon instanciation to extract a default
            configuration from that file. If no path is supplied,
            the configuration will initialize empty.
    """
    def __init__(self, config_file_path=None):
        self.configuration = {}

        if config_file_path is None:
            return

        try:
            with open(config_file_path, 'r') as config_file:
                self._parse_configuration(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("Configuration file not found, empty configuration!")

    def _parse_configuration(self, configuration_content):
        for line in configuration_content.readlines():
            line = line.strip()

            # Whitespace lines
            if not line:
                continue

            try:
                self.set(*line.split('='))
            except KeyError:
                raise KeyError("Configuration from file failed at line: \"%s\"" % line)

    def get(self, configuration_item):
        """
            Returns the configuration item with the given name
                or None if the item does not exist.
        """
        return self.configuration.get(configuration_item, None)

    def set(self, item_name, item_value):
        """
            Attemts to set an item of the configuration.
            Raises KeyError if item is already set.
        """
        if self.get(item_name) is not None:
            raise KeyError("Item already exists")

        self.configuration[item_name] = item_value

if __name__ == "__main__":
    CONFIG = Config("./configuration/.env")
    # CONFIG.set("database.host", "127.0.0.1")
    # CONFIG.set("database.host", "localhost")
    print(CONFIG.configuration)
    print(CONFIG.get("database.host"))
