"""
Shared data models for the calculator module.
"""

from dataclasses import dataclass, field


@dataclass
class CostResult:
    """Result of a cost calculation for a single component."""
    service: str
    component: str
    subtotal: float
    formula: str
    unit_price: str
    usage: str
    assumptions: list[str] = field(default_factory=list)
