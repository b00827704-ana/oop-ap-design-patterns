"""
Builder Pattern - HR Employee Onboarding system (refactored version)

Before: create_employee() took 17 positional arguments (telescoping constructor).
After:  an Employee data class + an EmployeeBuilder with small chainable methods,
        plus a preset builder (DeveloperBuilder).
"""

from dataclasses import dataclass, field
from datetime import date


# ---------------------------------------------------------------------------
# 1. The Product: a simple data container (17 attributes)
# ---------------------------------------------------------------------------
@dataclass
class Employee:
    # 7 required (no default value)
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str = field(default_factory=lambda: date.today().isoformat())
    # 10 optional (default values)
    manager_id: int | None = None
    phone: str | None = None
    address: str | None = None
    emergency_contact: str | None = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: str | None = None
    contract_type: str = "permanent"


# ---------------------------------------------------------------------------
# 2. The Builder: 8 chainable methods + _validate + build
# ---------------------------------------------------------------------------
class EmployeeBuilder:
    def __init__(self):
        self._data = {}          # values are collected here until build()

    def with_name(self, first_name: str, last_name: str) -> "EmployeeBuilder":
        self._data["first_name"] = first_name
        self._data["last_name"] = last_name
        return self              # returning self allows chaining

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._data["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float) -> "EmployeeBuilder":
        self._data["department"] = department
        self._data["position"] = position
        self._data["salary"] = salary
        return self

    def with_start_date(self, start_date: str) -> "EmployeeBuilder":
        self._data["start_date"] = start_date
        return self

    def with_contact(self, phone: str = None, address: str = None,
                     emergency_contact: str = None) -> "EmployeeBuilder":
        self._data["phone"] = phone
        self._data["address"] = address
        self._data["emergency_contact"] = emergency_contact
        return self

    def with_equipment(self, laptop: bool = False, parking: bool = False) -> "EmployeeBuilder":
        self._data["has_laptop"] = laptop
        self._data["has_parking"] = parking
        return self

    def with_access(self, vpn: bool = False, admin: bool = False) -> "EmployeeBuilder":
        self._data["has_vpn_access"] = vpn
        self._data["has_admin_rights"] = admin
        return self

    def with_work_details(self, manager_id: int = None, office_location: str = None,
                          contract_type: str = "permanent") -> "EmployeeBuilder":
        self._data["manager_id"] = manager_id
        self._data["office_location"] = office_location
        self._data["contract_type"] = contract_type
        return self

    def _validate(self) -> None:
        """Private: checks the required information, used only by build()."""
        if not self._data.get("first_name") or not self._data.get("last_name"):
            raise ValueError("Name is required")
        email = self._data.get("email")
        if not email or "@" not in email:
            raise ValueError("Valid email is required")
        if "department" not in self._data:
            raise ValueError("Job (department, position, salary) is required")
        if self._data["salary"] < 0:
            raise ValueError("Salary cannot be negative")

    def build(self) -> Employee:
        """Public: the last step. Validate, then create the Employee."""
        self._validate()
        return Employee(**self._data)


# ---------------------------------------------------------------------------
# 3. The Preset: a ready-made senior developer profile
# ---------------------------------------------------------------------------
class DeveloperBuilder(EmployeeBuilder):
    """Only name and email are needed; the rest of the profile is pre-filled.
    This fixes the 'hidden logic' problem: a Senior Developer ALWAYS gets admin rights."""

    def __init__(self, first_name: str, last_name: str, email: str, salary: float = 75000):
        super().__init__()                       # creates self._data
        (self.with_name(first_name, last_name)
             .with_email(email)
             .with_job("Engineering", "Senior Developer", salary)
             .with_equipment(laptop=True, parking=False)
             .with_access(vpn=True, admin=True)
             .with_work_details(office_location="Paris HQ"))


# ---------------------------------------------------------------------------
# Usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Fluent, readable creation (the intern from the old code)
    intern = (
        EmployeeBuilder()
        .with_name("Jane", "Smith")
        .with_email("jane.smith@company.com")
        .with_job("Marketing", "Intern", 15000)
        .with_start_date("2024-02-01")
        .with_equipment(laptop=True)
        .with_work_details(manager_id=42, office_location="Paris HQ", contract_type="internship")
        .build()
    )
    print(intern)

    # Preset: only name and email
    dev = DeveloperBuilder("John", "Doe", "john.doe@company.com").build()
    print(dev)

    # Preset + extra details chained before build
    dev2 = (DeveloperBuilder("Ana", "Petrovic", "ana@company.com")
            .with_contact(phone="+33612345678")
            .with_start_date("2024-01-15")
            .build())
    print(dev2)

    # Validation still works
    try:
        EmployeeBuilder().with_name("Bob", "Lee").with_email("not-an-email").build()
    except ValueError as error:
        print("Error:", error)
