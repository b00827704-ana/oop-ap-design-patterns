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
- (to do)

## Structural patterns

### Adapter – Reporting system (`structural/adapter`)
- (to do)