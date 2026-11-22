"""
Template Method Pattern - Data ETL pipelines (refactored version)

Before: CSVPipeline, APIPipeline and DatabasePipeline each rewrote the whole workflow
        (connect, extract, transform, validate, load, cleanup) in their own run().
After:  an abstract DataProcessPipeline writes the workflow ONCE in run() (the
        template method) plus the common steps; each pipeline only implements
        what is unique to its source.
"""

import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------
# Abstract base class: the recipe + the common steps
# ---------------------------------------------------------------------------
class DataProcessPipeline(ABC):
    def __init__(self, source: str):
        self._source = source      # protected (#): used by the children
        self._data = None

    # ----- the TEMPLATE METHOD: fixed order, never overridden -----
    def run(self) -> str:
        self._connect()
        self._extract()
        print(f"Extracted {len(self._data)} records")
        self._transform()
        print("Transformation complete")
        self._validate()
        self._before_load()        # hook: optional extra step
        self._load()
        self._cleanup()
        return f"{self.__class__.__name__} finished"

    # ----- abstract steps: every child MUST implement them -----
    @abstractmethod
    def _connect(self) -> None:
        """Open the connection to the source."""

    @abstractmethod
    def _extract(self) -> None:
        """Read the raw records into self._data."""

    @abstractmethod
    def _transform(self) -> None:
        """Clean and convert self._data."""

    @abstractmethod
    def _required_fields(self) -> list:
        """Fields every record must contain (used by _validate)."""

    # ----- common steps: written ONCE for all pipelines -----
    def _validate(self) -> None:
        print("Validating data...")
        required = self._required_fields()
        for record in self._data:
            if any(field not in record for field in required):
                raise ValueError(f"Invalid record structure: {record}")
        print("Validation passed")

    def _load(self) -> None:
        print("Loading data to destination...")
        time.sleep(0.5)
        print(f"Loaded {len(self._data)} records successfully")

    def _cleanup(self) -> None:
        print("Cleaning up resources...")
        self._data = None
        print("Cleanup complete")

    # ----- hook: does nothing by default, children MAY override it -----
    def _before_load(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Concrete pipelines: only what is unique
# ---------------------------------------------------------------------------
class CSVPipeline(DataProcessPipeline):
    def _connect(self) -> None:
        print(f"Connecting to CSV file: {self._source}")
        time.sleep(0.5)
        print("CSV connection established")

    def _extract(self) -> None:
        print("Extracting data from CSV...")
        self._data = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]

    def _transform(self) -> None:
        print("Transforming CSV data...")
        for record in self._data:
            record["age"] = int(record["age"])
            record["name"] = record["name"].upper()

    def _required_fields(self) -> list:
        return ["id", "name"]


class APIPipeline(DataProcessPipeline):
    def _connect(self) -> None:
        print(f"Connecting to API: {self._source}")
        time.sleep(0.5)
        print("API connection established")

    def _extract(self) -> None:
        print("Extracting data from API...")
        self._data = [
            {"user_id": 101, "username": "charlie", "score": 85},
            {"user_id": 102, "username": "diana", "score": 92},
        ]

    def _transform(self) -> None:
        print("Transforming API data...")
        for record in self._data:
            record["score"] = int(record["score"])
            record["username"] = record["username"].lower()
            record["grade"] = "A" if record["score"] >= 90 else "B"

    def _required_fields(self) -> list:
        return ["user_id", "username"]


class DatabasePipeline(DataProcessPipeline):
    def _connect(self) -> None:
        print(f"Connecting to database: {self._source}")
        time.sleep(0.5)
        print("Database connection established")

    def _extract(self) -> None:
        print("Extracting data from database...")
        self._data = [
            {"product_id": 501, "product_name": "Laptop", "price": 1200},
            {"product_id": 502, "product_name": "Mouse", "price": 25},
        ]

    def _transform(self) -> None:
        print("Transforming database data...")
        for record in self._data:
            record["price"] = float(record["price"])
            record["product_name"] = record["product_name"].title()
            record["tax"] = record["price"] * 0.2

    def _required_fields(self) -> list:
        return ["product_id", "price"]

    def _before_load(self) -> None:          # this pipeline uses the hook
        print("Opening a database transaction before loading")


# NEW pipeline: same workflow, only XML-specific extraction and transformation
class XMLPipeline(DataProcessPipeline):
    SAMPLE_XML = """
    <orders>
        <order><order_id>9001</order_id><customer>eva</customer><amount>59.90</amount></order>
        <order><order_id>9002</order_id><customer>frank</customer><amount>120</amount></order>
    </orders>
    """

    def _connect(self) -> None:
        print(f"Opening XML file: {self._source}")
        time.sleep(0.5)
        print("XML file opened")

    def _extract(self) -> None:
        print("Extracting data from XML...")
        root = ET.fromstring(self.SAMPLE_XML)
        self._data = [{child.tag: child.text for child in order} for order in root]

    def _transform(self) -> None:
        print("Transforming XML data...")
        for record in self._data:
            record["order_id"] = int(record["order_id"])
            record["amount"] = float(record["amount"])
            record["customer"] = record["customer"].capitalize()

    def _required_fields(self) -> list:
        return ["order_id", "amount"]


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pipelines = [
        ("CSV", CSVPipeline("data/users.csv")),
        ("API", APIPipeline("https://api.example.com/users")),
        ("DATABASE", DatabasePipeline("postgresql://localhost/mydb")),
        ("XML (NEW!)", XMLPipeline("data/orders.xml")),
    ]
    for label, pipeline in pipelines:
        print(f"RUNNING {label} PIPELINE")
        print("=" * 70)
        result = pipeline.run()
        print(f"\n{result}\n")
        