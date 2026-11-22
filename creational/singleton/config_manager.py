"""
Singleton Pattern - Configuration manager (refactored version)

Before: every function called load_config(), so config.json was read again each time
        and every module had its own separate copy of the configuration.
After:  ONE ConfigManager instance reads the file once; every service shares it.
"""

import json
from pathlib import Path

# config.json is looked for next to this file, so the script works from any folder
CONFIG_PATH = Path(__file__).parent / "config.json"


# ---------------------------------------------------------------------------
# The Singleton
# ---------------------------------------------------------------------------
class ConfigManager:
    _instance = None              # class attribute: remembers the ONE object (None = not created yet)

    def __new__(cls):
        """Runs when ConfigManager() is called. Creates the object only the first time."""
        if cls._instance is None:                 # first call?
            cls._instance = super().__new__(cls)  # create the object...
            cls._instance._load_config()          # ...and read the file ONCE
        return cls._instance                      # every call returns the same object

    def _load_config(self) -> None:
        """Private: opens and reads config.json (the old load_config function)."""
        print(f"Loading config from {CONFIG_PATH.name}...")
        with open(CONFIG_PATH, "r") as f:
            self._config = json.load(f)

    def get(self, key: str, default=None):
        """Read a nested value with dots, e.g. get("database.host")."""
        value = self._config
        for part in key.split("."):               # "database.host" -> ["database", "host"]
            if not isinstance(value, dict) or part not in value:
                return default                    # missing key -> safe default
            value = value[part]
        return value

    def reload(self) -> None:
        """Safety net: re-read the file (e.g. after editing it) without creating a new instance."""
        self._load_config()

    @classmethod
    def get_instance(cls) -> "ConfigManager":
        """Global access point, as asked in the mission."""
        return cls()                              # goes through __new__ -> same object


# ---------------------------------------------------------------------------
# The services: they USE the ConfigManager (no inheritance)
# Every load_config() call is replaced by ConfigManager.get_instance()
# ---------------------------------------------------------------------------
class DatabaseService:
    def __init__(self):
        self.config = ConfigManager.get_instance()

    def connect(self) -> None:
        db_host = self.config.get("database.host")
        db_port = self.config.get("database.port")
        print(f"Connecting to database at {db_host}:{db_port}")


class EmailService:
    def __init__(self):
        self.config = ConfigManager.get_instance()

    def send(self, to: str, subject: str) -> None:
        smtp_host = self.config.get("email.smtp_host")
        sender = self.config.get("email.sender")
        print(f"Sending '{subject}' to {to} from {sender} via {smtp_host}")


class PaymentService:
    def __init__(self):
        self.config = ConfigManager.get_instance()

    def process(self, amount: float) -> None:
        environment = self.config.get("payment.environment")
        print(f"Processing {amount}€ in {environment} mode")


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    DatabaseService().connect()
    EmailService().send("user@test.com", "Welcome")
    PaymentService().process(99.99)

    # Proof: there is only ONE instance
    config1 = ConfigManager.get_instance()
    config2 = ConfigManager.get_instance()
    print("Same instance:", config1 is config2)

    # Missing key -> default value instead of a crash
    print("Missing key:", config1.get("database.user", "admin"))
    