"""
Amazon Bedrock AgentCore Gateway pricing.

Sources:
- https://aws.amazon.com/bedrock/agentcore/pricing/

AgentCore Gateway provides serverless tool serving for agents.
Pricing is per-request based.

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class GatewayPricing:
    """AgentCore Gateway pricing."""
    per_million_requests: float  # $/million requests


# AgentCore Gateway pricing (us-east-1)
GATEWAY_PRICING = GatewayPricing(
    per_million_requests=2.00,
)
