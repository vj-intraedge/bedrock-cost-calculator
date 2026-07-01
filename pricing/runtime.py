"""
Amazon Bedrock AgentCore Runtime pricing.

Sources:
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://rywalker.com/research/agentcore-code-interpreter

Consumption-based, billed per second with 1-second minimum.
I/O wait and idle time are free.

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class RuntimePricing:
    """AgentCore Runtime pricing."""
    vcpu_per_hour: float  # $/vCPU-hour
    memory_per_gb_hour: float  # $/GB-hour


# AgentCore Runtime pricing (us-east-1)
RUNTIME_PRICING = RuntimePricing(
    vcpu_per_hour=0.0895,
    memory_per_gb_hour=0.00945,
)
