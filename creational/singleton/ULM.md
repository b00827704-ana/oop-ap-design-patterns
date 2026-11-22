# Singleton Pattern – Configuration manager

```mermaid
classDiagram
    class ConfigManager {
        -_instance: ConfigManager
        -_config: dict
        +#95;#95;new#95;#95;(cls) ConfigManager
        -_load_config() None
        +get(key: str, default) Any
        +reload() None
        +get_instance() ConfigManager
    }

    class DatabaseService {
        -config: ConfigManager
        +connect() None
    }
    class EmailService {
        -config: ConfigManager
        +send(to: str, subject: str) None
    }
    class PaymentService {
        -config: ConfigManager
        +process(amount: float) None
    }

    note for ConfigManager "Only ONE instance: the first get_instance() reads config.json, later calls return the same object"

    DatabaseService ..> ConfigManager : uses
    EmailService ..> ConfigManager : uses
    PaymentService ..> ConfigManager : uses
```
