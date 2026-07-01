"""
AWS Lambda pricing.

Sources:
- https://aws.amazon.com/lambda/pricing/

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class LambdaPricing:
    """Lambda pricing components."""
    request_per_million: float  # $/million requests
    gb_second: float  # $/GB-second of compute


# Lambda pricing (us-east-1, x86)
LAMBDA_PRICING = LambdaPricing(
    request_per_million=0.20,
    gb_second=0.0000166667,
)
