"""
Amazon Bedrock Knowledge Base pricing.

Sources:
- https://aws.amazon.com/bedrock/pricing/
- https://markaicode.com/pricing/aws-bedrock-pricing-api-cost-production/

Region: us-east-1 (N. Virginia)
Last updated: 2025-07
"""

from dataclasses import dataclass


@dataclass
class KBPricing:
    """Knowledge Base pricing components."""
    # Storage
    storage_per_gb_month: float  # $/GB-month for managed vector store

    # Embedding (Titan Text Embedding V2)
    embedding_per_million_tokens: float  # $/1M tokens

    # Retrieval
    retrieval_per_1000_queries: float  # $/1000 retrieval queries

    # Sync / Ingestion
    sync_per_1000_objects: float  # $/1000 objects synced

    # Web Crawler (additional data source cost)
    crawler_per_1000_urls: float  # $/1000 URLs crawled


# Bedrock Knowledge Base pricing (us-east-1)
KB_PRICING = KBPricing(
    storage_per_gb_month=0.10,
    embedding_per_million_tokens=0.02,
    retrieval_per_1000_queries=0.035,
    sync_per_1000_objects=0.01,
    crawler_per_1000_urls=0.35,
)
