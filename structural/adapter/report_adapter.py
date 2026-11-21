"""
Adapter Pattern - Reporting system (refactored version)

Before: every function converted the legacy XML to JSON by hand (and even "cheated"
        by dumping the original dict, ignoring the XML).
After:  a ReportGeneratorInterface (the contract) + a LegacyReportAdapter that wraps
        the old system and translates its XML into JSON in ONE place.
"""

import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Existing classes: we are NOT allowed to modify them
# ---------------------------------------------------------------------------
class LegacyReportGenerator:
    """Adaptee: old external library, only speaks XML."""

    def generate_report(self, data: dict) -> str:
        """Returns XML format - old system"""
        xml = "<report>\n"
        for key, value in data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</report>"
        return xml


class AnalyticsDashboard:
    """Client: only understands JSON."""

    def display(self, json_data: str) -> None:
        data = json.loads(json_data)
        print("=== Analytics Dashboard ===")
        for key, value in data.items():
            print(f"  {key}: {value}")


# ---------------------------------------------------------------------------
# 1. The interface (the contract): what the client expects
# ---------------------------------------------------------------------------
class ReportGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        """Must return the report as a JSON string."""


# ---------------------------------------------------------------------------
# 2. The adapter: implements the interface and wraps the legacy system
# ---------------------------------------------------------------------------
class LegacyReportAdapter(ReportGeneratorInterface):
    def __init__(self, legacy: LegacyReportGenerator):
        self._legacy = legacy                         # wrap the old object (don't inherit from it)

    def generate(self, data: dict) -> str:
        xml_report = self._legacy.generate_report(data)   # let the old system do the real work
        return self._xml_to_json(xml_report)              # then translate its answer

    def _xml_to_json(self, xml: str) -> str:
        """Private: the conversion lives in ONE place only."""
        root = ET.fromstring(xml)                     # parse the XML text into a tree
        result = {child.tag: self._parse_value(child.text) for child in root}
        return json.dumps(result)

    @staticmethod
    def _parse_value(text: str):
        """XML stores everything as text: turn '1234' back into 1234."""
        for cast in (int, float):
            try:
                return cast(text)
            except (TypeError, ValueError):
                pass
        return text


# ---------------------------------------------------------------------------
# 3. Business logic: no conversion code here anymore
# ---------------------------------------------------------------------------
def show_report(generator: ReportGeneratorInterface, dashboard: AnalyticsDashboard, data: dict) -> None:
    dashboard.display(generator.generate(data))


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Adapter wraps the legacy system
    report_generator = LegacyReportAdapter(LegacyReportGenerator())
    dashboard = AnalyticsDashboard()

    # Dashboard doesn't know it's talking to a legacy system
    show_report(report_generator, dashboard,
                {"total_sales": 150000, "orders": 1234, "avg_order": 121.55})
    show_report(report_generator, dashboard,
                {"total_items": 5000, "low_stock": 45, "out_of_stock": 12}) 