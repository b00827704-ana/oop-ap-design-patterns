"""
Strategy Pattern - Multi-format report generator (refactored version)

Before: ReportGenerator chose the format with two if/elif chains (one to build
        the content, one to save the file) driven by a format string.
After:  one class per format behind a FormatStrategy interface. ReportGenerator
        (the context) holds ONE strategy and can switch it at runtime.
"""

import json
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# 1. Strategy interface: the contract every format must follow
# ---------------------------------------------------------------------------
class FormatStrategy(ABC):
    @abstractmethod
    def format(self, data: list) -> str:
        """Build the report content from the data."""

    @abstractmethod
    def get_extension(self) -> str:
        """File extension used when saving, e.g. '.pdf'."""


# ---------------------------------------------------------------------------
# 2. Concrete strategies: one class per format
# ---------------------------------------------------------------------------
class PDFFormatStrategy(FormatStrategy):
    def format(self, data: list) -> str:
        report = "PDF REPORT\n"
        report += "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\n"
        report += "End of PDF Report"
        return report

    def get_extension(self) -> str:
        return ".pdf"


class ExcelFormatStrategy(FormatStrategy):
    def format(self, data: list) -> str:
        report = "EXCEL REPORT\n"
        report += "-" * 50 + "\n"
        report += "Name\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report

    def get_extension(self) -> str:
        return ".xlsx"


class CSVFormatStrategy(FormatStrategy):
    def format(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report

    def get_extension(self) -> str:
        return ".csv"


class JSONFormatStrategy(FormatStrategy):
    def format(self, data: list) -> str:
        return json.dumps(data, indent=2)

    def get_extension(self) -> str:
        return ".json"


# NEW format added WITHOUT modifying any existing class (Open/Closed)
class HTMLFormatStrategy(FormatStrategy):
    def format(self, data: list) -> str:
        rows = "\n".join(
            f"    <tr><td>{item['name']}</td><td>{item['value']}</td></tr>" for item in data
        )
        return (
            "<table>\n"
            "    <tr><th>Name</th><th>Value</th></tr>\n"
            f"{rows}\n"
            "</table>"
        )

    def get_extension(self) -> str:
        return ".html"


# ---------------------------------------------------------------------------
# 3. Context: holds one strategy and uses it (no if/elif anymore)
# ---------------------------------------------------------------------------
class ReportGenerator:
    def __init__(self, data: list, strategy: FormatStrategy = None):
        self._data = data
        self._strategy = strategy

    def set_strategy(self, strategy: FormatStrategy) -> None:
        """Switch the format at runtime."""
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No format strategy set: call set_strategy() first")
        return self._strategy.format(self._data)          # delegate to the strategy

    def save_report(self, filename: str) -> None:
        """Common saving logic, written ONCE; only the extension comes from the strategy."""
        path = filename + self._strategy.get_extension()
        with open(path, "w") as f:
            f.write(self.generate_report())
        print(f"Report saved to {path}")


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]

    generator = ReportGenerator(data)

    print("=== PDF FORMAT ===")
    generator.set_strategy(PDFFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== CSV FORMAT ===")                      # switch format dynamically
    generator.set_strategy(CSVFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== JSON FORMAT ===")
    generator.set_strategy(JSONFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== HTML FORMAT (NEW!) ===")
    generator.set_strategy(HTMLFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    generator.set_strategy(CSVFormatStrategy())
    generator.save_report("sales_report")
    