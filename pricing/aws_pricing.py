"""
Centralized AWS pricing provider.

This module serves as the single source of truth for all pricing data.
Prices are hardcoded from official AWS pricing pages.

Sources:
- https://aws.amazon.com/bedrock/pricing/
- https://aws.amazon.com/bedrock/agentcore/pricing/
- https://aws.amazon.com/lambda/pricing/
- https://aws.amazon.com/api-gateway/pricing/

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from pricing.models import MODELS, ModelPricing
from pricing.kb import KB_PRICING, KBPricing
from pricing.runtime import RUNTIME_PRICING, RuntimePricing
from pricing.gateway import GATEWAY_PRICING, GatewayPricing
from pricing.lambda_ import LAMBDA_PRICING, LambdaPricing
from pricing.apigateway import APIGATEWAY_PRICING, APIGatewayPricing


class AWSPricingProvider:
    """
    Provides normalized pricing data from hardcoded AWS prices.

    Usage:
        provider = AWSPricingProvider()
        model = provider.get_model_pricing("Nova Micro")
        kb = provider.get_kb_pricing()
    """

    REGION = "us-east-1"
    PRICING_SOURCE = "AWS Official Pricing Pages"
    LAST_UPDATED = "2025-07"

    def get_model_pricing(self, model_name: str) -> ModelPricing:
        """Get pricing for a specific LLM model."""
        if model_name not in MODELS:
            raise ValueError(f"Unknown model: {model_name}. Available: {list(MODELS.keys())}")
        return MODELS[model_name]

    def get_all_models(self) -> dict[str, ModelPricing]:
        """Get pricing for all available models."""
        return MODELS

    def get_model_names(self) -> list[str]:
        """Get list of available model names."""
        return list(MODELS.keys())

    def get_kb_pricing(self) -> KBPricing:
        """Get Knowledge Base pricing."""
        return KB_PRICING

    def get_runtime_pricing(self) -> RuntimePricing:
        """Get AgentCore Runtime pricing."""
        return RUNTIME_PRICING

    def get_gateway_pricing(self) -> GatewayPricing:
        """Get AgentCore Gateway pricing."""
        return GATEWAY_PRICING

    def get_lambda_pricing(self) -> LambdaPricing:
        """Get Lambda pricing."""
        return LAMBDA_PRICING

    def get_apigateway_pricing(self) -> APIGatewayPricing:
        """Get API Gateway pricing."""
        return APIGATEWAY_PRICING
