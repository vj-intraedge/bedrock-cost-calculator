"""
AgentCore Runtime & Gateway cost calculator.
Also includes Lambda and API Gateway infrastructure costs.
"""

from calculator.models import CostResult
from pricing.aws_pricing import AWSPricingProvider


def calculate_agentcore_costs(
    provider: AWSPricingProvider,
    sessions_per_month: int,
    messages_per_session: int,
) -> list[CostResult]:
    """
    Calculate AgentCore Runtime and Gateway costs.

    Assumptions:
    - Each message triggers one Runtime invocation
    - Runtime uses 0.25 vCPU, 0.5 GB memory, ~5 seconds per invocation
    - Gateway handles tool routing for each message
    """
    runtime = provider.get_runtime_pricing()
    gateway = provider.get_gateway_pricing()
    results = []

    total_messages = sessions_per_month * messages_per_session

    # --- Runtime ---
    vcpu_per_invocation = 0.25  # vCPU
    memory_per_invocation_gb = 0.5  # GB
    seconds_per_invocation = 5.0

    hours_per_invocation = seconds_per_invocation / 3600

    vcpu_cost = total_messages * vcpu_per_invocation * hours_per_invocation * runtime.vcpu_per_hour
    memory_cost = total_messages * memory_per_invocation_gb * hours_per_invocation * runtime.memory_per_gb_hour
    runtime_total = vcpu_cost + memory_cost

    results.append(CostResult(
        service="AgentCore",
        component="Runtime (vCPU)",
        subtotal=vcpu_cost,
        formula=(
            f"{total_messages:,} invocations × {vcpu_per_invocation} vCPU × "
            f"{seconds_per_invocation}s ÷ 3600 × ${runtime.vcpu_per_hour}/vCPU-hr = "
            f"${vcpu_cost:.4f}"
        ),
        unit_price=f"${runtime.vcpu_per_hour}/vCPU-hour",
        usage=f"{total_messages:,} invocations × {seconds_per_invocation}s",
        assumptions=[
            f"{vcpu_per_invocation} vCPU per invocation",
            f"{seconds_per_invocation}s average duration",
            "Billed per second, 1s minimum",
        ],
    ))

    results.append(CostResult(
        service="AgentCore",
        component="Runtime (Memory)",
        subtotal=memory_cost,
        formula=(
            f"{total_messages:,} invocations × {memory_per_invocation_gb} GB × "
            f"{seconds_per_invocation}s ÷ 3600 × ${runtime.memory_per_gb_hour}/GB-hr = "
            f"${memory_cost:.4f}"
        ),
        unit_price=f"${runtime.memory_per_gb_hour}/GB-hour",
        usage=f"{total_messages:,} invocations × {memory_per_invocation_gb} GB",
        assumptions=[
            f"{memory_per_invocation_gb} GB memory per invocation",
            "I/O wait and idle time are free",
        ],
    ))

    # --- Gateway ---
    gateway_cost = (total_messages / 1_000_000) * gateway.per_million_requests
    results.append(CostResult(
        service="AgentCore",
        component="Gateway",
        subtotal=gateway_cost,
        formula=(
            f"{total_messages:,} requests ÷ 1M × ${gateway.per_million_requests}/M = "
            f"${gateway_cost:.6f}"
        ),
        unit_price=f"${gateway.per_million_requests}/million requests",
        usage=f"{total_messages:,} requests",
        assumptions=["1 gateway request per message"],
    ))

    return results


def calculate_infrastructure_costs(
    provider: AWSPricingProvider,
    sessions_per_month: int,
    messages_per_session: int,
    lambda_duration_seconds: float,
    lambda_memory_mb: int,
    api_gateway_requests: int,
) -> list[CostResult]:
    """
    Calculate Lambda, API Gateway, and related infrastructure costs.
    """
    lambda_pricing = provider.get_lambda_pricing()
    apigw_pricing = provider.get_apigateway_pricing()
    results = []

    total_messages = sessions_per_month * messages_per_session

    # --- Lambda ---
    # Requests
    lambda_request_cost = (total_messages / 1_000_000) * lambda_pricing.request_per_million

    # Compute (GB-seconds)
    memory_gb = lambda_memory_mb / 1024
    gb_seconds = total_messages * memory_gb * lambda_duration_seconds
    lambda_compute_cost = gb_seconds * lambda_pricing.gb_second

    lambda_total = lambda_request_cost + lambda_compute_cost

    results.append(CostResult(
        service="Infrastructure",
        component="Lambda (Requests)",
        subtotal=lambda_request_cost,
        formula=(
            f"{total_messages:,} requests ÷ 1M × ${lambda_pricing.request_per_million}/M = "
            f"${lambda_request_cost:.4f}"
        ),
        unit_price=f"${lambda_pricing.request_per_million}/million requests",
        usage=f"{total_messages:,} invocations",
        assumptions=["1 Lambda invocation per message"],
    ))

    results.append(CostResult(
        service="Infrastructure",
        component="Lambda (Compute)",
        subtotal=lambda_compute_cost,
        formula=(
            f"{total_messages:,} invocations × {memory_gb:.3f} GB × {lambda_duration_seconds}s = "
            f"{gb_seconds:,.1f} GB-s × ${lambda_pricing.gb_second}/GB-s = "
            f"${lambda_compute_cost:.4f}"
        ),
        unit_price=f"${lambda_pricing.gb_second}/GB-second",
        usage=f"{gb_seconds:,.1f} GB-seconds",
        assumptions=[
            f"Lambda memory: {lambda_memory_mb} MB",
            f"Average duration: {lambda_duration_seconds}s",
        ],
    ))

    # --- API Gateway ---
    apigw_cost = (api_gateway_requests / 1_000_000) * apigw_pricing.rest_per_million_requests
    results.append(CostResult(
        service="Infrastructure",
        component="API Gateway",
        subtotal=apigw_cost,
        formula=(
            f"{api_gateway_requests:,} requests ÷ 1M × "
            f"${apigw_pricing.rest_per_million_requests}/M = ${apigw_cost:.4f}"
        ),
        unit_price=f"${apigw_pricing.rest_per_million_requests}/million REST API calls",
        usage=f"{api_gateway_requests:,} requests",
        assumptions=["REST API type"],
    ))

    # --- CloudWatch ---
    # Estimate: 5 log events per message, each ~1KB
    log_events = total_messages * 5
    log_gb = log_events * 0.001 / 1024  # 1KB each -> GB
    cloudwatch_ingestion_per_gb = 0.50  # $/GB ingested
    cloudwatch_cost = log_gb * cloudwatch_ingestion_per_gb
    results.append(CostResult(
        service="Infrastructure",
        component="CloudWatch Logs",
        subtotal=cloudwatch_cost,
        formula=(
            f"{total_messages:,} msgs × 5 log events × 1KB = "
            f"{log_gb:.4f} GB × ${cloudwatch_ingestion_per_gb}/GB = ${cloudwatch_cost:.4f}"
        ),
        unit_price=f"${cloudwatch_ingestion_per_gb}/GB ingested",
        usage=f"{log_gb:.4f} GB logs",
        assumptions=[
            "~5 log events per message",
            "~1KB per log event",
        ],
    ))

    # --- Data Transfer ---
    # Estimate: 2KB response per message
    data_transfer_gb = total_messages * 2 / (1024 * 1024)  # 2KB per msg -> GB
    data_transfer_cost = data_transfer_gb * apigw_pricing.data_transfer_per_gb
    results.append(CostResult(
        service="Infrastructure",
        component="Data Transfer",
        subtotal=data_transfer_cost,
        formula=(
            f"{total_messages:,} msgs × 2KB = {data_transfer_gb:.4f} GB × "
            f"${apigw_pricing.data_transfer_per_gb}/GB = ${data_transfer_cost:.4f}"
        ),
        unit_price=f"${apigw_pricing.data_transfer_per_gb}/GB (first 10TB)",
        usage=f"{data_transfer_gb:.4f} GB",
        assumptions=["~2KB average response size"],
    ))

    return results
