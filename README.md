# oop-ap-design-patterns
# OOP Design Patterns – Exercises

Ana Petrovic AIDAMS 2A
Pattern exercises from the OOP System Design course
Each folder contains the refactored code and its UML class diagram (`UML.md`).

## Creational patterns

### Factory – Payment system (`creational/factory`)
- **Problem:** one big `process_payment()` function with `if/elif` for each payment type.
  Adding a new method meant modifying the function (breaks Open/Closed).
- **Solution:** an abstract `PaymentProcessor` (the contract), one class per payment method,
  and a `PaymentFactory` that uses a dictionary to return the right processor.
- **Result:** a new payment method = a new class + `register_processor()`, no existing code changed.

### Builder – HR onboarding (`creational/builder`)
- **Problem:** `create_employee()` took 17 positional arguments (telescoping constructor).
- **Solution:** an `Employee` dataclass, an `EmployeeBuilder` with chainable `with_...()` methods,
  validation in one place (`build()`), and a `DeveloperBuilder` preset.
- **Result:** readable creation, no argument-order bugs, and a Senior Developer always gets admin rights, without others forgetting to add it manually.

### Singleton – Configuration manager (`creational/singleton`)
- **Problem:** every function called `load_config()`, so `config.json` was opened and read
  again each time (4 times for one run). Each function also had its own separate copy of the config.
- **Solution:** a `ConfigManager` class that creates **only one instance**. The first call to
  `get_instance()` creates it and reads the file; every later call returns the same object
  without reading the file again. Values are read with `get("database.host")`.
- **Result:** the file is loaded once, all services share the same configuration,
  a change made by one service is seen by all, and tests have a single point to replace with a fake config.

## Structural patterns

### Adapter – Reporting system (`structural/adapter`)
- **Problem:** the legacy library returns XML, the dashboard only reads JSON, and the conversion was copied by hand in every function. The legacy code cannot be modified.
- **Solution:** a `ReportGeneratorInterface` (the contract: `generate()` returns JSON) and a
  `LegacyReportAdapter` that implements it, wraps the legacy generator, and translates XML to JSON in one private method.
- **Result:** the dashboard never sees XML, the conversion lives in one place, and the old system stays untouched. 

### Decorator – Order pricing (`structural/decorator`)
- **Problem:** one `calculate_total()` method with 5 boolean flags; every new option meant editing the method, and the order of operations was hidden.
- **Solution:** an `OrderComponent` interface, a `BaseOrder`, and an abstract `OrderDecorator` that wraps an order. Each option (shipping, insurance, gift wrap, discount, premium) is its own decorator that adds its cost and description, then delegates to the wrapped order.
- **Result:** no flags, one class per option (SRP), new options without touching existing code (OCP), and the stacking order is visible in the code.
The client does not know if his order has been decorated or not, it is one iterface for all (instead of creting new interfaces). Also, each decorator handles one fucntion, so it was easier to test and modify them without affecting the overall function of the interface.


## Behavioral patterns

### Strategy – Multi-format reports (`behavioral/strategy`)
- **Problem:** `ReportGenerator` chose the format with if/elif chains in two methods
  (one to build the content, one to save the file). Adding a format (XML, Markdown)
  meant changing existing code (breaks Open/Closed), one class handled four formats
  (breaks Single Responsibility), a single format could not be tested alone, a typo
  in the format string ("Csv") silently returned "Unknown format", and the format had
  to be passed as a string on every call.
- **Solution:** a `FormatStrategy` interface (`format(data)` and `get_extension()`),
  one class per format (PDF, Excel, CSV, JSON), and a `ReportGenerator` context that
  holds one strategy and can switch it with `set_strategy()`. The file-saving code is
  written once; only the extension comes from the strategy.
- **Result:** no if/elif chains, each format isolated and testable, formats can be
  changed at runtime, and a new HTML format was added without modifying any existing class.