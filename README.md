# oop-ap-design-patterns
# OOP Design Patterns – Exercises

AIDAMS 2A
Refactoring exercises from the OOP / System Design course
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