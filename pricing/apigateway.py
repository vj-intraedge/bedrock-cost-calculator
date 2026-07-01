"""
Amazon API Gateway pricing.

Sources:
- https://aws.amazon.com/api-gateway/pricing/
- https://costgoat.com/pricing/amazon-api-gateway

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class APIGatewayPricing:
    """API Gateway pricing (REST APIs)."""
    rest_per_million_requests: float  # $/million REST API calls
    data_transfer_per_gb: float  # $/GB data transferred out (first 10TB)


# API Gateway pricing (us-east-1)
APIGATEWAY_PRICING = APIGatewayPricing(
    rest_per_million_requests=3.50,
    data_transfer_per_gb=0.09,
)
