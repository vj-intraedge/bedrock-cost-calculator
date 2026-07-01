"""
LLM Model pricing data from Amazon Bedrock.

Prices are per 1M tokens, sourced from:
- https://aws.amazon.com/bedrock/pricing/
- https://futureagi.com/llm-cost-calculator/bedrock/
- https://gist.github.com/pahud/2af7b03d6838366fa2fd6337029688a5

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class ModelPricing:
    """Pricing for a single LLM model."""
    name: str
    provider: str
    input_price_per_million: float  # $ per 1M input tokens
    output_price_per_million: float  # $ per 1M output tokens
    context_window: int  # max tokens
    max_output_tokens: int


# All prices in USD per 1M tokens, us-east-1
MODELS: dict[str, ModelPricing] = {
    "Gemma 3 4B": ModelPricing(
        name="Gemma 3 4B",
        provider="Google",
        input_price_per_million=0.04,
        output_price_per_million=0.08,
        context_window=128_000,
        max_output_tokens=8_192,
    ),
    "Nova Micro": ModelPricing(
        name="Nova Micro",
        provider="Amazon",
        input_price_per_million=0.035,
        output_price_per_million=0.14,
        context_window=128_000,
        max_output_tokens=10_000,
    ),
    "GPT-OSS-20B": ModelPricing(
        name="GPT-OSS-20B",
        provider="OpenAI",
        input_price_per_million=0.07,
        output_price_per_million=0.20,
        context_window=128_000,
        max_output_tokens=16_000,
    ),
    "GLM 4.7 Flash": ModelPricing(
        name="GLM 4.7 Flash",
        provider="Zhipu AI",
        input_price_per_million=0.07,
        output_price_per_million=0.40,
        context_window=200_000,
        max_output_tokens=131_000,
    ),
}
