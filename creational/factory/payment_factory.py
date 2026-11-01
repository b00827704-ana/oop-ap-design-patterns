"""
Factory Pattern - Payment system (refactored version)

Before: one big process_payment() function with if/elif for every payment type
After:  one class per payment type and a factory that picks the right class
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. The Interface (the blueprint / the contract)
# ---------------------------------------------------------------------------
class PaymentProcessor(ABC):
    """Every payment processor MUST implement validate() and process()."""

    name: str = ""             # identifier, e.g. "credit_card"
    error_message: str = ""    # message returned when validation fails

    @abstractmethod
    def validate(self, details: dict) -> bool:
        """Return True if the payment details are valid."""

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        """Process the payment and return the result as a dictionary."""

    # Small helpers shared by all processors (avoid repeating ourselves)
    def _success(self, amount: float, fee: float) -> dict:
        return {"success": True, "method": self.name, "amount": amount + fee, "fee": fee}

    def _failure(self) -> dict:
        return {"success": False, "error": self.error_message}


# ---------------------------------------------------------------------------
# 2. Concrete Implementations (one class = one payment method)
# ---------------------------------------------------------------------------
class CreditCardProcessor(PaymentProcessor):
    name = "credit_card"
    error_message = "Invalid card number or CVV"
    FEE_RATE = 0.029           # 2.9%

    def validate(self, details: dict) -> bool:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        return bool(card_number) and len(card_number) == 16 \
            and bool(cvv) and len(cvv) == 3

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return self._failure()
        fee = amount * self.FEE_RATE
        return self._success(amount, fee)


class BankTransferProcessor(PaymentProcessor):
    name = "bank_transfer"
    error_message = "Invalid IBAN"
    FLAT_FEE = 1.50            # 1.50€

    def validate(self, details: dict) -> bool:
        iban = details.get("iban")
        return bool(iban) and len(iban) >= 15

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return self._failure()
        return self._success(amount, self.FLAT_FEE)


class PayPalProcessor(PaymentProcessor):
    name = "paypal"
    error_message = "Invalid PayPal email"
    FEE_RATE = 0.034           # 3.4%
    FIXED_FEE = 0.30           # + 0.30€

    def validate(self, details: dict) -> bool:
        email = details.get("email")
        return bool(email) and "@" in email

    def process(self, amount: float, details: dict) -> dict:
        if not self.validate(details):
            return self._failure()
        fee = amount * self.FEE_RATE + self.FIXED_FEE
        return self._success(amount, fee)


# ---------------------------------------------------------------------------
# 3. The Factory (the middleman)
# ---------------------------------------------------------------------------
class PaymentFactory:
    """Takes a string like "paypal" and returns the matching processor."""

    def __init__(self):
        # Dictionary: string -> class (no if/elif chain!)
        self._processors = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor,
        }

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        processor_class = self._processors.get(payment_type)
        if processor_class is None:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return processor_class()   # create and return an instance

    def register_processor(self, payment_type: str, processor_class: type) -> None:
        """Add a new payment method WITHOUT modifying this class (Open/Closed)."""
        self._processors[payment_type] = processor_class


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    factory = PaymentFactory()

    # Credit card
    processor = factory.get_processor("credit_card")
    print(processor.process(100.0, {"card_number": "1234567890123456", "cvv": "123"}))

    # Bank transfer
    processor = factory.get_processor("bank_transfer")
    print(processor.process(100.0, {"iban": "FR7630006000011234567890189", "bic": "BNPAFRPP"}))

    # PayPal
    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "user@example.com"}))

    # Invalid details
    processor = factory.get_processor("paypal")
    print(processor.process(100.0, {"email": "not-an-email"}))

    # Unknown payment type
    try:
        factory.get_processor("bitcoin")
    except ValueError as error:
        print(error)

    # Adding a new method later: new class + register it, nothing else changes
    class ApplePayProcessor(PaymentProcessor):
        name = "apple_pay"
        error_message = "Invalid Apple Pay token"

        def validate(self, details: dict) -> bool:
            return bool(details.get("token"))

        def process(self, amount: float, details: dict) -> dict:
            if not self.validate(details):
                return self._failure()
            return self._success(amount, 0.0)

    factory.register_processor("apple_pay", ApplePayProcessor)
    print(factory.get_processor("apple_pay").process(100.0, {"token": "abc123"}))