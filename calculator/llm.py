"""
LLM inference cost calculator.

Computes monthly costs for input and output token usage
based on selected model and traffic parameters.
"""

from calculator.models import CostResult
from pricing.aws_pricing import AWSPricingProvider


def calculate_llm_costs(
    provider: AWSPricingProvider,
    model_name: str,
    sessions_per_month: int,
    messages_per_session: int,
    input_tokens_per_message: int,
    output_tokens_per_message: int,
) -> list[CostResult]:
    """
    Calculate LLM inference costs.

    Returns a list of CostResult for input tokens and output tokens.
    """
    model = provider.get_model_pricing(model_name)
    total_messages = sessions_per_month * messages_per_session

    # Input tokens
    total_input_tokens = total_messages * input_tokens_per_message
    input_cost = (total_input_tokens / 1_000_000) * model.input_price_per_million

    # Output tokens
    total_output_tokens = total_messages * output_tokens_per_message
    output_cost = (total_output_tokens / 1_000_000) * model.output_price_per_million

    results = [
        CostResult(
            service="LLM Inference",
            component="Input Tokens",
            subtotal=input_cost,
            formula=(
                f"{sessions_per_month:,} sessions × {messages_per_session} msgs × "
                f"{input_tokens_per_message:,} tokens = {total_input_tokens:,} tokens × "
                f"${model.input_price_per_million}/M = ${input_cost:.4f}"
            ),
            unit_price=f"${model.input_price_per_million}/M tokens",
            usage=f"{total_input_tokens:,} tokens",
            assumptions=[
                f"Model: {model_name} ({model.provider})",
                f"On-demand pricing, us-east-1",
            ],
        ),
        CostResult(
            service="LLM Inference",
            component="Output Tokens",
            subtotal=output_cost,
            formula=(
                f"{sessions_per_month:,} sessions × {messages_per_session} msgs × "
                f"{output_tokens_per_message:,} tokens = {total_output_tokens:,} tokens × "
                f"${model.output_price_per_million}/M = ${output_cost:.4f}"
            ),
            unit_price=f"${model.output_price_per_million}/M tokens",
            usage=f"{total_output_tokens:,} tokens",
            assumptions=[
                f"Model: {model_name} ({model.provider})",
                f"On-demand pricing, us-east-1",
            ],
        ),
    ]

    return results
