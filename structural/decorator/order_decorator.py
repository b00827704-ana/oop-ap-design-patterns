"""
Decorator Pattern - Order pricing system (refactored version)

Before: one calculate_total() method with 5 boolean flags and a chain of ifs.
After:  each option is its own small class that WRAPS an order, adds its cost and
        description line, and delegates the rest to the order inside (Russian dolls).
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. The interface: what every order looks like to the client
# ---------------------------------------------------------------------------
class OrderComponent(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        """Total price of the order so far."""

    @abstractmethod
    def get_description(self) -> str:
        """Breakdown of the order, one line per item."""


# ---------------------------------------------------------------------------
# 2. The concrete component: the plain order we decorate
# ---------------------------------------------------------------------------
class BaseOrder(OrderComponent):
    def __init__(self, base_price: float):
        self._base_price = base_price

    def get_cost(self) -> float:
        return self._base_price

    def get_description(self) -> str:
        return f"Base price: {self._base_price:.2f}€"


# ---------------------------------------------------------------------------
# 3. The abstract decorator: IS an OrderComponent and HAS an OrderComponent
# ---------------------------------------------------------------------------
class OrderDecorator(OrderComponent, ABC):
    def __init__(self, order: OrderComponent):
        self._order = order                        # protected (#): the wrapped order

    def get_cost(self) -> float:                   # default: just delegate
        return self._order.get_cost()

    def get_description(self) -> str:
        return self._order.get_description()


# ---------------------------------------------------------------------------
# 4. Concrete decorators: each adds ONE thing, then delegates
# ---------------------------------------------------------------------------
class ExpressShippingDecorator(OrderDecorator):
    COST = 15.00                                   # static value: no constructor needed

    def get_cost(self) -> float:
        return self._order.get_cost() + self.COST

    def get_description(self) -> str:
        return self._order.get_description() + f"\nExpress shipping: +{self.COST:.2f}€"


class InsuranceDecorator(OrderDecorator):
    RATE = 0.05                                    # 5% of the order cost so far

    def _insurance(self) -> float:
        return self._order.get_cost() * self.RATE

    def get_cost(self) -> float:
        return self._order.get_cost() + self._insurance()

    def get_description(self) -> str:
        return self._order.get_description() + f"\nInsurance (5%): +{self._insurance():.2f}€"


class GiftWrapDecorator(OrderDecorator):
    COST = 5.00

    def get_cost(self) -> float:
        return self._order.get_cost() + self.COST

    def get_description(self) -> str:
        return self._order.get_description() + f"\nGift wrap: +{self.COST:.2f}€"


class DiscountDecorator(OrderDecorator):
    def __init__(self, order: OrderComponent, percent: float):
        super().__init__(order)                    # run OrderDecorator's __init__ -> sets self._order
        self._percent = percent                    # dynamic value: changes per order

    def _discount(self) -> float:
        return self._order.get_cost() * self._percent / 100

    def get_cost(self) -> float:
        return self._order.get_cost() - self._discount()

    def get_description(self) -> str:
        return self._order.get_description() + f"\nDiscount ({self._percent:g}%): -{self._discount():.2f}€"


class PremiumMemberDecorator(OrderDecorator):
    RATE = 0.10

    def _discount(self) -> float:
        return self._order.get_cost() * self.RATE

    def get_cost(self) -> float:
        return self._order.get_cost() - self._discount()

    def get_description(self) -> str:
        return self._order.get_description() + f"\nPremium member (10%): -{self._discount():.2f}€"


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Simple order
    simple = BaseOrder(100.00)
    print(simple.get_description())
    print(f"Total: {simple.get_cost():.2f}€")

    print("\n---\n")

    # Build order with decorators - readable and flexible
    order = BaseOrder(100.00)
    order = ExpressShippingDecorator(order)
    order = InsuranceDecorator(order)
    order = GiftWrapDecorator(order)
    order = DiscountDecorator(order, percent=15)
    order = PremiumMemberDecorator(order)

    print(order.get_description())
    print(f"Total: {order.get_cost():.2f}€")