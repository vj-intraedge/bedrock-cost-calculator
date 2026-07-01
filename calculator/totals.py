"""
Total cost aggregation and scenario management.
"""

from dataclasses import dataclass, field
from calculator.models import CostResult
from calculator.llm import calculate_llm_costs
from calculator.kb import calculate_kb_costs
from calculator.runtime import calculate_agentcore_costs, calculate_infrastructure_costs
from pricing.aws_pricing import AWSPricingProvider


@dataclass
class CostSummary:
    """Aggregated cost summary."""
    monthly_total: float
    annual_total: float
    cost_per_session: float
    cost_per_message: float
    breakdown_by_service: dict[str, float]
    all_results: list[CostResult]


def calculate_total_costs(
    model_name: str,
    sessions_per_month: int,
    messages_per_session: int,
    input_tokens_per_message: int,
    output_tokens_per_message: int,
    kb_queries_per_message: int,
    kb_size_gb: float,
    crawl_frequency: str,
    lambda_duration_seconds: float,
    lambda_memory_mb: int,
    api_gateway_requests: int,
) -> CostSummary:
    """
    Calculate all costs and return a summary.
    """
    provider = AWSPricingProvider()
    all_results: list[CostResult] = []

    # LLM costs
    llm_results = calculate_llm_costs(
        provider=provider,
        model_name=model_name,
        sessions_per_month=sessions_per_month,
        messages_per_session=messages_per_session,
        input_tokens_per_message=input_tokens_per_message,
        output_tokens_per_message=output_tokens_per_message,
    )
    all_results.extend(llm_results)

    # KB costs (only if queries > 0)
    if kb_queries_per_message > 0:
        kb_results = calculate_kb_costs(
            provider=provider,
            sessions_per_month=sessions_per_month,
            messages_per_session=messages_per_session,
            kb_queries_per_message=kb_queries_per_message,
            kb_size_gb=kb_size_gb,
            crawl_frequency=crawl_frequency,
            input_tokens_per_message=input_tokens_per_message,
        )
        all_results.extend(kb_results)

    # AgentCore costs
    agentcore_results = calculate_agentcore_costs(
        provider=provider,
        sessions_per_month=sessions_per_month,
        messages_per_session=messages_per_session,
    )
    all_results.extend(agentcore_results)

    # Infrastructure costs
    infra_results = calculate_infrastructure_costs(
        provider=provider,
        sessions_per_month=sessions_per_month,
        messages_per_session=messages_per_session,
        lambda_duration_seconds=lambda_duration_seconds,
        lambda_memory_mb=lambda_memory_mb,
        api_gateway_requests=api_gateway_requests,
    )
    all_results.extend(infra_results)

    # Aggregate
    monthly_total = sum(r.subtotal for r in all_results)
    total_messages = sessions_per_month * messages_per_session

    breakdown: dict[str, float] = {}
    for r in all_results:
        breakdown[r.service] = breakdown.get(r.service, 0.0) + r.subtotal

    return CostSummary(
        monthly_total=monthly_total,
        annual_total=monthly_total * 12,
        cost_per_session=monthly_total / max(sessions_per_month, 1),
        cost_per_message=monthly_total / max(total_messages, 1),
        breakdown_by_service=breakdown,
        all_results=all_results,
    )
